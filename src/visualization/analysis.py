"""
Comparison Analyzer - Analiză comparativă între algoritmi
Student B - Generarea graficelor pentru documentație
"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from PIL import Image


class ComparisonAnalyzer:
    """
    Creează grafice comparative între Simulated Annealing și Genetic Algorithm.
    """
    
    def __init__(self):
        """Inițializează analizorul."""
        self.results = {}
    
    def add_result(self, algorithm_name: str, history: dict, final_solution, target_image):
        """
        Adaugă rezultatele unui algoritm.
        
        Args:
            algorithm_name: "SA" sau "GA"
            history: Dicționarul cu istoricul algoritmului
            final_solution: Soluția finală
            target_image: Imaginea țintă
        """
        from ..core.renderer import render_solution
        from ..core.fitness import calculate_pixel_accuracy
        
        final_image = render_solution(final_solution)
        accuracy = calculate_pixel_accuracy(final_image, target_image)
        
        self.results[algorithm_name] = {
            'history': history,
            'solution': final_solution,
            'image': final_image,
            'accuracy': accuracy
        }
    
    def generate_comparison_report(self, output_path: str = "results/comparison_report.png"):
        """
        Generează un raport vizual complet cu toate graficele.
        
        Args:
            output_path: Calea unde să salveze raportul
        """
        if len(self.results) < 2:
            print("⚠️ Nu sunt suficiente rezultate pentru comparație!")
            return
        
        # Creăm o figură mare cu multiple subploturi
        fig = plt.figure(figsize=(18, 12))
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # Titlu general
        fig.suptitle('Analiză Comparativă: Simulated Annealing vs Genetic Algorithm', 
                     fontsize=16, fontweight='bold')
        
        # --- RÂNDUL 1: Imaginile ---
        
        # Original
        ax_original = fig.add_subplot(gs[0, 0])
        if 'SA' in self.results:
            # Presupunem că avem target_image undeva
            ax_original.set_title('Imaginea Originală', fontsize=12, fontweight='bold')
            ax_original.axis('off')
        
        # SA Result
        if 'SA' in self.results:
            ax_sa_img = fig.add_subplot(gs[0, 1])
            ax_sa_img.imshow(self.results['SA']['image'])
            ax_sa_img.set_title(
                f"Simulated Annealing\nAcuratețe: {self.results['SA']['accuracy']:.2f}%",
                fontsize=12, fontweight='bold', color='blue'
            )
            ax_sa_img.axis('off')
        
        # GA Result
        if 'GA' in self.results:
            ax_ga_img = fig.add_subplot(gs[0, 2])
            ax_ga_img.imshow(self.results['GA']['image'])
            ax_ga_img.set_title(
                f"Genetic Algorithm\nAcuratețe: {self.results['GA']['accuracy']:.2f}%",
                fontsize=12, fontweight='bold', color='green'
            )
            ax_ga_img.axis('off')
        
        # --- RÂNDUL 2: Convergență Fitness ---
        
        ax_fitness = fig.add_subplot(gs[1, :])
        ax_fitness.set_title('Comparație Convergență (Fitness vs Timp)', fontsize=12, fontweight='bold')
        ax_fitness.set_xlabel('Timp (secunde)', fontsize=10)
        ax_fitness.set_ylabel('RMSE (Eroare)', fontsize=10)
        ax_fitness.grid(True, alpha=0.3)
        
        if 'SA' in self.results:
            sa_history = self.results['SA']['history']
            ax_fitness.plot(
                sa_history['time'],
                sa_history['fitness'],
                'b-', linewidth=2, label='Simulated Annealing', alpha=0.8
            )
        
        if 'GA' in self.results:
            ga_history = self.results['GA']['history']
            ax_fitness.plot(
                ga_history['time'],
                ga_history['best_fitness'],
                'g-', linewidth=2, label='Genetic Algorithm', alpha=0.8
            )
        
        ax_fitness.legend(fontsize=10)
        
        # --- RÂNDUL 3: Metrici specifice ---
        
        # SA: Temperatura
        if 'SA' in self.results:
            ax_temp = fig.add_subplot(gs[2, 0])
            sa_history = self.results['SA']['history']
            ax_temp.plot(sa_history['temperature'], 'b-', linewidth=2)
            ax_temp.set_title('SA: Evoluția Temperaturii', fontsize=11, fontweight='bold')
            ax_temp.set_xlabel('Progres')
            ax_temp.set_ylabel('Temperatura')
            ax_temp.grid(True, alpha=0.3)
        
        # SA: Acceptance Rate
        if 'SA' in self.results:
            ax_accept = fig.add_subplot(gs[2, 1])
            sa_history = self.results['SA']['history']
            ax_accept.plot(sa_history['acceptance_rate'], 'b-', linewidth=2)
            ax_accept.set_title('SA: Rata de Acceptare', fontsize=11, fontweight='bold')
            ax_accept.set_xlabel('Progres')
            ax_accept.set_ylabel('Acceptance Rate')
            ax_accept.set_ylim([0, 1])
            ax_accept.grid(True, alpha=0.3)
        
        # GA: Diversitate
        if 'GA' in self.results:
            ax_diversity = fig.add_subplot(gs[2, 2])
            ga_history = self.results['GA']['history']
            ax_diversity.plot(ga_history['diversity'], 'g-', linewidth=2)
            ax_diversity.set_title('GA: Diversitatea Populației', fontsize=11, fontweight='bold')
            ax_diversity.set_xlabel('Generații')
            ax_diversity.set_ylabel('Diversitate')
            ax_diversity.grid(True, alpha=0.3)
        
        # Salvăm figura
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n📊 Raport complet salvat: {output_path}")
        
        plt.show()
    
    def generate_summary_table(self):
        """
        Generează un tabel text cu comparația finală.
        """
        print("\n" + "="*70)
        print(" " * 20 + "TABEL COMPARATIV FINAL")
        print("="*70)
        print(f"{'Metric':<30} | {'SA':>15} | {'GA':>15}")
        print("-"*70)
        
        if 'SA' in self.results and 'GA' in self.results:
            sa = self.results['SA']
            ga = self.results['GA']
            
            # Acuratețe
            print(f"{'Acuratețe Finală (%)':<30} | {sa['accuracy']:>15.2f} | {ga['accuracy']:>15.2f}")
            
            # Fitness final
            sa_final_fitness = sa['history']['fitness'][-1] if sa['history']['fitness'] else 0
            ga_final_fitness = ga['history']['best_fitness'][-1] if ga['history']['best_fitness'] else 0
            print(f"{'RMSE Final':<30} | {sa_final_fitness:>15.2f} | {ga_final_fitness:>15.2f}")
            
            # Timp total
            sa_time = sa['history']['time'][-1] if sa['history']['time'] else 0
            ga_time = ga['history']['time'][-1] if ga['history']['time'] else 0
            print(f"{'Timp Total (secunde)':<30} | {sa_time:>15.2f} | {ga_time:>15.2f}")
            
            # Câștigător
            print("-"*70)
            if sa['accuracy'] > ga['accuracy']:
                winner = "SA (Mai Precis)"
            elif ga['accuracy'] > sa['accuracy']:
                winner = "GA (Mai Precis)"
            else:
                winner = "Egalitate"
            
            if sa_time < ga_time:
                faster = "SA (Mai Rapid)"
            elif ga_time < sa_time:
                faster = "GA (Mai Rapid)"
            else:
                faster = "Egalitate"
            
            print(f"{'Câștigător Acuratețe':<30} | {winner:>32}")
            print(f"{'Câștigător Viteză':<30} | {faster:>32}")
        
        print("="*70 + "\n")
    
    def save_final_images(self, output_dir: str = "results"):
        """
        Salvează imaginile finale separate.
        
        Args:
            output_dir: Directorul unde să salveze imaginile
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for alg_name, data in self.results.items():
            filename = f"{output_dir}/{alg_name}_final.png"
            data['image'].save(filename)
            print(f"💾 Salvat: {filename}")
