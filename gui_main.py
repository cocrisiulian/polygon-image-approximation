"""
Interfață grafică (GUI) pentru proiectul de aproximare a imaginilor.
Permite selectarea imaginii, alegerea algoritmilor și generarea rapoartelor Excel.

Funcționalități:
- Selector de imagine (Browse) + buton pentru Mona Lisa
- Alegere algoritm: SA, GA sau Ambii (în paralel)
- Configurare parametri
- Export automat în Excel cu 3 foi de calcul
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import sys
from datetime import datetime
import concurrent.futures
import traceback

# Importăm componentele proiectului
from src.algorithms import SimulatedAnnealing, GeneticAlgorithm
from src.visualization import LiveDisplay, ResultPlotter
from src.core import render_solution
from src.utils import ExcelExporter, AlgorithmLogger, LogCapture


class PolygonApproximationGUI:
    """Interfață grafică pentru aproximarea imaginilor cu poligoane."""
    
    def __init__(self, root):
        """
        Inițializează interfața grafică.
        
        Args:
            root: Fereastra principală Tkinter
        """
        self.root = root
        self.root.title("🎨 Aproximare Imagini cu Poligoane - SA vs GA")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variabile
        self.image_path = tk.StringVar()
        self.algorithm_choice = tk.StringVar(value="both")
        self.num_polygons = tk.IntVar(value=30)
        self.target_image = None
        self.is_processing = False
        
        # Parametri SA
        self.sa_temp = tk.DoubleVar(value=100.0)
        self.sa_cooling = tk.DoubleVar(value=0.995)
        self.sa_iterations = tk.IntVar(value=10000)
        
        # Parametri GA
        self.ga_population = tk.IntVar(value=20)
        self.ga_generations = tk.IntVar(value=1000)
        self.ga_mutation = tk.DoubleVar(value=0.1)
        
        # Rezultate
        self.sa_results = None
        self.ga_results = None
        
        # Logger și plotter
        self.logger = None
        self.result_plotter = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Creează toate widget-urile interfeței."""
        
        # === HEADER ===
        header_frame = tk.Frame(self.root, bg="#366092", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎨 APROXIMARE IMAGINI CU POLIGOANE",
            font=("Arial", 18, "bold"),
            bg="#366092",
            fg="white"
        )
        title_label.pack(pady=25)
        
        # === MAIN CONTAINER ===
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === SECȚIUNEA 1: Selectare Imagine ===
        image_frame = tk.LabelFrame(
            main_container,
            text="📷 Selectare Imagine",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        image_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Cale imagine
        path_frame = tk.Frame(image_frame, bg="#f0f0f0")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(path_frame, text="Imagine:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        path_entry = tk.Entry(path_frame, textvariable=self.image_path, width=50, font=("Arial", 10))
        path_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Butoane selectare
        buttons_frame = tk.Frame(image_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X)
        
        browse_btn = tk.Button(
            buttons_frame,
            text="📂 Browse...",
            command=self._browse_image,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        mona_lisa_btn = tk.Button(
            buttons_frame,
            text="🖼️ Mona Lisa",
            command=self._load_mona_lisa,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        mona_lisa_btn.pack(side=tk.LEFT)
        
        # === SECȚIUNEA 2: Alegere Algoritm ===
        algo_frame = tk.LabelFrame(
            main_container,
            text="🔧 Configurare Algoritm",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        algo_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Alegere algoritm
        tk.Label(algo_frame, text="Algoritm:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        algo_options_frame = tk.Frame(algo_frame, bg="#f0f0f0")
        algo_options_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Radiobutton(
            algo_options_frame,
            text="🔥 Simulated Annealing (SA)",
            variable=self.algorithm_choice,
            value="sa",
            bg="#f0f0f0",
            font=("Arial", 10),
            command=self._update_params_visibility
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            algo_options_frame,
            text="🧬 Genetic Algorithm (GA)",
            variable=self.algorithm_choice,
            value="ga",
            bg="#f0f0f0",
            font=("Arial", 10),
            command=self._update_params_visibility
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            algo_options_frame,
            text="⚡ Ambii (în paralel)",
            variable=self.algorithm_choice,
            value="both",
            bg="#f0f0f0",
            font=("Arial", 10),
            command=self._update_params_visibility
        ).pack(side=tk.LEFT)
        
        # Număr poligoane
        polygons_frame = tk.Frame(algo_frame, bg="#f0f0f0")
        polygons_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(polygons_frame, text="Număr poligoane:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        tk.Spinbox(
            polygons_frame,
            from_=10,
            to=200,
            textvariable=self.num_polygons,
            width=10,
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        # === SECȚIUNEA 3: Parametri Algoritmi ===
        params_notebook = ttk.Notebook(main_container)
        params_notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Tab SA
        sa_tab = tk.Frame(params_notebook, bg="#f0f0f0", padx=15, pady=15)
        params_notebook.add(sa_tab, text="🔥 Parametri SA")
        
        sa_params = [
            ("Temperatură inițială:", self.sa_temp, 1.0, 1000.0),
            ("Rată răcire:", self.sa_cooling, 0.9, 0.999),
            ("Iterații maxime:", self.sa_iterations, 100, 50000),
        ]
        
        for i, (label_text, var, min_val, max_val) in enumerate(sa_params):
            frame = tk.Frame(sa_tab, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label_text, bg="#f0f0f0", font=("Arial", 10), width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            if isinstance(var, tk.IntVar):
                tk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var, width=15, font=("Arial", 10)).pack(side=tk.LEFT)
            else:
                tk.Entry(frame, textvariable=var, width=15, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Tab GA
        ga_tab = tk.Frame(params_notebook, bg="#f0f0f0", padx=15, pady=15)
        params_notebook.add(ga_tab, text="🧬 Parametri GA")
        
        ga_params = [
            ("Mărime populație:", self.ga_population, 10, 100),
            ("Generații maxime:", self.ga_generations, 100, 5000),
            ("Rată mutație:", self.ga_mutation, 0.01, 0.5),
        ]
        
        for i, (label_text, var, min_val, max_val) in enumerate(ga_params):
            frame = tk.Frame(ga_tab, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label_text, bg="#f0f0f0", font=("Arial", 10), width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            if isinstance(var, tk.IntVar):
                tk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var, width=15, font=("Arial", 10)).pack(side=tk.LEFT)
            else:
                tk.Entry(frame, textvariable=var, width=15, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # === SECȚIUNEA 4: Buton Start & Progress ===
        control_frame = tk.Frame(main_container, bg="#f0f0f0")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶️ START PROCESARE",
            command=self._start_processing,
            bg="#2196F3",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=40,
            pady=15,
            cursor="hand2"
        )
        self.start_btn.pack()
        
        # Progress bar
        self.progress_frame = tk.Frame(main_container, bg="#f0f0f0")
        self.progress_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            bg="#f0f0f0",
            font=("Arial", 10),
            fg="#366092"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        
        # === SECȚIUNEA 5: Butoane Rezultate ===
        results_frame = tk.Frame(main_container, bg="#f0f0f0")
        results_frame.pack(fill=tk.X, pady=(10, 0))
        
        results_label = tk.Label(
            results_frame,
            text="📊 După procesare:",
            bg="#f0f0f0",
            font=("Arial", 10, "bold")
        )
        results_label.pack(anchor=tk.W, pady=(0, 5))
        
        buttons_frame = tk.Frame(results_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X)
        
        self.view_graphs_btn = tk.Button(
            buttons_frame,
            text="📈 Vizualizează Grafice",
            command=self._show_graphs,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.view_graphs_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_sa_log_btn = tk.Button(
            buttons_frame,
            text="📄 Log SA",
            command=lambda: self._show_log('sa'),
            bg="#FF5722",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.view_sa_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_ga_log_btn = tk.Button(
            buttons_frame,
            text="📄 Log GA",
            command=lambda: self._show_log('ga'),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.view_ga_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_combined_log_btn = tk.Button(
            buttons_frame,
            text="📄 Log Combined",
            command=lambda: self._show_log('combined'),
            bg="#607D8B",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.view_combined_log_btn.pack(side=tk.LEFT)
        
    def _browse_image(self):
        """Deschide dialog pentru selectarea imaginii."""
        filename = filedialog.askopenfilename(
            title="Selectează imaginea",
            filetypes=[
                ("Imagini", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Toate fișierele", "*.*")
            ]
        )
        if filename:
            self.image_path.set(filename)
    
    def _load_mona_lisa(self):
        """Încarcă imaginea Mona Lisa."""
        mona_path = "images/mona_lisa.jpg"
        if os.path.exists(mona_path):
            self.image_path.set(mona_path)
        else:
            messagebox.showerror("Eroare", f"Imaginea Mona Lisa nu a fost găsită la: {mona_path}")
    
    def _update_params_visibility(self):
        """Actualizează vizibilitatea parametrilor în funcție de algoritm."""
        pass  # Ambele tab-uri rămân vizibile
    
    def _prepare_image(self, image_path: str, max_size: int = 200) -> Image.Image:
        """
        Pregătește imaginea pentru procesare.
        
        Args:
            image_path: Calea către imagine
            max_size: Dimensiunea maximă
        
        Returns:
            Image.Image: Imaginea pregătită
        """
        img = Image.open(image_path).convert('RGB')
        
        # Redimensionăm pentru performanță
        width, height = img.size
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        return img
    
    def _show_log(self, log_type: str):
        """
        Afișează fișierul de log într-o fereastră separată.
        
        Args:
            log_type: Tipul de log ('sa', 'ga', 'combined')
        """
        if not self.logger:
            messagebox.showwarning("Atenție", "Nu există log-uri disponibile!")
            return
        
        log_paths = self.logger.get_log_paths()
        log_path = log_paths.get(log_type)
        
        if not log_path or not os.path.exists(log_path):
            messagebox.showwarning("Atenție", f"Fișierul de log {log_type} nu există!")
            return
        
        # Creează fereastră nouă
        log_window = tk.Toplevel(self.root)
        log_window.title(f"📄 Log {log_type.upper()}")
        log_window.geometry("800x600")
        
        # Text widget cu scrollbar
        text_frame = tk.Frame(log_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 9)
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Citește și afișează conținutul
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert(1.0, content)
                text_widget.config(state=tk.DISABLED)  # Read-only
        except Exception as e:
            text_widget.insert(1.0, f"Eroare la citirea log-ului: {e}")
        
        # Buton refresh
        refresh_btn = tk.Button(
            log_window,
            text="🔄 Reîmprospătează",
            command=lambda: self._refresh_log(text_widget, log_path),
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        refresh_btn.pack(pady=(0, 10))
    
    def _refresh_log(self, text_widget, log_path):
        """Reîmprospătează conținutul log-ului."""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert(1.0, content)
        except Exception as e:
            text_widget.insert(1.0, f"Eroare la citirea log-ului: {e}")
        text_widget.config(state=tk.DISABLED)
    
    def _show_graphs(self):
        """Afișează graficele finale."""
        if not self.result_plotter:
            messagebox.showwarning("Atenție", "Nu există grafice disponibile!")
            return
        
        try:
            self.result_plotter.plot_results(
                target_image=self.target_image,
                sa_results=self.sa_results,
                ga_results=self.ga_results,
                save_path="results/grafice_finale.png"
            )
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la afișarea graficelor: {e}")
    
    def _start_processing(self):
        """Pornește procesarea în thread separat."""
        if self.is_processing:
            messagebox.showwarning("Atenție", "Procesare deja în curs!")
            return
        
        if not self.image_path.get():
            messagebox.showerror("Eroare", "Vă rugăm să selectați o imagine!")
            return
        
        if not os.path.exists(self.image_path.get()):
            messagebox.showerror("Eroare", f"Fișierul nu există: {self.image_path.get()}")
            return
        
        # Pregătim imaginea
        try:
            self.target_image = self._prepare_image(self.image_path.get())
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea imaginii: {e}")
            return
        
        # Dezactivăm butonul și pornim progress bar
        self.start_btn.config(state=tk.DISABLED, bg="#CCCCCC")
        self.progress_label.config(text="🔄 Procesare în curs...")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        
        self.is_processing = True
        
        # Inițializăm logger-ul
        self.logger = AlgorithmLogger()
        self.result_plotter = ResultPlotter()
        
        # Rulăm în thread separat
        thread = threading.Thread(target=self._run_algorithms, daemon=True)
        thread.start()
    
    def _run_algorithms(self):
        """Rulează algoritmii selectați."""
        choice = self.algorithm_choice.get()
        
        try:
            self.logger.log_general(f"====== SESIUNE NOUĂ ======")
            self.logger.log_general(f"Imagine: {os.path.basename(self.image_path.get())}")
            self.logger.log_general(f"Poligoane: {self.num_polygons.get()}")
            self.logger.log_general(f"Algoritm: {choice}")
            self.logger.log_general("")
            
            if choice == "both":
                # Rulăm ambii algoritmi în paralel
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_sa = executor.submit(self._run_sa)
                    future_ga = executor.submit(self._run_ga)
                    
                    self.sa_results = future_sa.result()
                    self.ga_results = future_ga.result()
            
            elif choice == "sa":
                self.sa_results = self._run_sa()
                self.ga_results = None
            
            elif choice == "ga":
                self.ga_results = self._run_ga()
                self.sa_results = None
            
            # Generăm raportul Excel
            self._generate_excel_report()
            
            # Închidem logger-ul
            if self.logger:
                self.logger.close()
            
            # Activăm butoanele de rezultate
            self.root.after(0, self._enable_result_buttons)
            
            # Afișăm mesaj de succes
            self.root.after(0, self._show_success)
            
        except Exception as e:
            error_msg = f"Eroare la procesare: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            if self.logger:
                self.logger.log_general(f"EROARE: {error_msg}")
                self.logger.close()
            self.root.after(0, lambda msg=error_msg: self._show_error(msg))
        
        finally:
            # Oprim progress bar și reactivăm butonul
            self.root.after(0, self._processing_complete)
    
    def _run_sa(self):
        """Rulează Simulated Annealing."""
        self.logger.log_sa("🔥 Pornire Simulated Annealing...")
        print("\n🔥 Pornire Simulated Annealing...")
        
        sa = SimulatedAnnealing(
            target_image=self.target_image,
            num_polygons=self.num_polygons.get(),
            initial_temperature=self.sa_temp.get(),
            cooling_rate=self.sa_cooling.get(),
            max_iterations=self.sa_iterations.get()
        )
        
        best_solution = sa.run()
        history_dict = sa.get_history()
        
        self.logger.log_sa(f"✅ Finalizat cu fitness: {history_dict.get('fitness', [0])[-1]:.2f}")
        
        # Salvăm imaginea rezultat
        result_img = render_solution(best_solution)
        os.makedirs("results", exist_ok=True)
        result_img.save("results/SA_final.png")
        
        # Convertim history din dict cu liste la listă de dict-uri
        history = []
        if history_dict and 'fitness' in history_dict:
            fitness_list = history_dict['fitness']
            temp_list = history_dict.get('temperature', [])
            acceptance_list = history_dict.get('acceptance_rate', [])
            time_list = history_dict.get('time', [])
            
            for i in range(len(fitness_list)):
                history.append({
                    'iteration': (i + 1) * 500,  # Presupunem log la fiecare 500 iterații
                    'fitness': fitness_list[i],
                    'temperature': temp_list[i] if i < len(temp_list) else 0,
                    'acceptance_rate': acceptance_list[i] if i < len(acceptance_list) else 0,
                    'time': time_list[i] if i < len(time_list) else 0
                })
        
        # Calculăm fitness final
        fitness_final = history_dict.get('fitness', [0])[-1] if history_dict and history_dict.get('fitness') else 0
        total_time = sum(history_dict.get('time', [])) if history_dict else 0
        
        return {
            'solution': best_solution,
            'history': history,
            'fitness_final': fitness_final,
            'total_time': total_time,
            'iterations': len(history_dict.get('fitness', [])) if history_dict else 0,
            'initial_temp': self.sa_temp.get(),
            'cooling_rate': self.sa_cooling.get(),
            'max_iterations': self.sa_iterations.get(),
        }
    
    def _run_ga(self):
        """Rulează Genetic Algorithm."""
        self.logger.log_ga("🧬 Pornire Genetic Algorithm...")
        print("\n🧬 Pornire Genetic Algorithm...")
        
        ga = GeneticAlgorithm(
            target_image=self.target_image,
            num_polygons=self.num_polygons.get(),
            population_size=self.ga_population.get(),
            num_generations=self.ga_generations.get(),
            mutation_rate=self.ga_mutation.get()
        )
        
        best_solution = ga.run()
        history_dict = ga.get_history()
        
        self.logger.log_ga(f"✅ Finalizat cu fitness: {history_dict.get('best_fitness', [0])[-1]:.2f}")
        
        # Salvăm imaginea rezultat
        result_img = render_solution(best_solution)
        os.makedirs("results", exist_ok=True)
        result_img.save("results/GA_final.png")
        
        # Convertim history din dict cu liste la listă de dict-uri
        history = []
        if history_dict and 'best_fitness' in history_dict:
            best_fitness_list = history_dict['best_fitness']
            avg_fitness_list = history_dict.get('avg_fitness', [])
            diversity_list = history_dict.get('diversity', [])
            time_list = history_dict.get('time', [])
            
            for i in range(len(best_fitness_list)):
                history.append({
                    'generation': (i + 1) * 50,  # Presupunem log la fiecare 50 generații
                    'best_fitness': best_fitness_list[i],
                    'avg_fitness': avg_fitness_list[i] if i < len(avg_fitness_list) else 0,
                    'diversity': diversity_list[i] if i < len(diversity_list) else 0,
                    'time': time_list[i] if i < len(time_list) else 0
                })
        
        # Calculăm fitness final
        fitness_final = history_dict.get('best_fitness', [0])[-1] if history_dict and history_dict.get('best_fitness') else 0
        total_time = sum(history_dict.get('time', [])) if history_dict else 0
        
        return {
            'solution': best_solution,
            'history': history,
            'fitness_final': fitness_final,
            'total_time': total_time,
            'generations': len(history_dict.get('best_fitness', [])) if history_dict else 0,
            'population_size': self.ga_population.get(),
            'max_generations': self.ga_generations.get(),
            'mutation_rate': self.ga_mutation.get(),
            'crossover_rate': 0.7,
            'elitism': 2,
        }
    
    def _generate_excel_report(self):
        """Generează raportul Excel."""
        print("\n📊 Generare raport Excel...")
        
        exporter = ExcelExporter(output_path="results/raport_comparative.xlsx")
        
        image_name = os.path.basename(self.image_path.get())
        
        exporter.export_results(
            image_name=image_name,
            num_polygons=self.num_polygons.get(),
            sa_results=self.sa_results,
            ga_results=self.ga_results
        )
    
    def _show_success(self):
        """Afișează mesaj de succes."""
        messagebox.showinfo(
            "Succes",
            "✅ Procesare completă!\n\n"
            "📊 Raport Excel: results/raport_comparative.xlsx\n"
            "🖼️ Imagini rezultat: results/\n"
            "📄 Log-uri: results/logs/\n"
            "📈 Grafice: Click 'Vizualizează Grafice'"
        )
    
    def _show_error(self, error_msg):
        """Afișează mesaj de eroare."""
        messagebox.showerror("Eroare", error_msg)
    
    def _enable_result_buttons(self):
        """Activează butoanele de rezultate."""
        self.view_graphs_btn.config(state=tk.NORMAL)
        
        choice = self.algorithm_choice.get()
        if choice == "sa" or choice == "both":
            self.view_sa_log_btn.config(state=tk.NORMAL)
        if choice == "ga" or choice == "both":
            self.view_ga_log_btn.config(state=tk.NORMAL)
        if choice == "both":
            self.view_combined_log_btn.config(state=tk.NORMAL)
    
    def _processing_complete(self):
        """Finalizează procesarea."""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
        self.start_btn.config(state=tk.NORMAL, bg="#2196F3")
        self.is_processing = False


def main():
    """Funcția principală pentru rularea GUI."""
    root = tk.Tk()
    app = PolygonApproximationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
