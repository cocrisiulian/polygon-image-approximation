"""
Live Display - Afișare în timp real a progresului
Student B - Vizualizare
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
from PIL import Image
import numpy as np
from ..core.renderer import render_solution


class LiveDisplay:
    """
    Afișează progresul algoritmului în timp real.
    """
    
    def __init__(self, target_image: Image.Image, algorithm_name: str = "Algorithm"):
        """
        Inițializează afișajul live.
        
        Args:
            target_image: Imaginea țintă
            algorithm_name: Numele algoritmului (pentru titlu)
        """
        self.target_image = target_image
        self.algorithm_name = algorithm_name
        
        # Creăm figura cu 3 subploturi
        self.fig = plt.figure(figsize=(15, 5))
        gs = gridspec.GridSpec(1, 3, figure=self.fig)
        
        # Subplot 1: Imaginea țintă
        self.ax_target = self.fig.add_subplot(gs[0, 0])
        self.ax_target.set_title('Imaginea Originală')
        self.ax_target.imshow(target_image)
        self.ax_target.axis('off')
        
        # Subplot 2: Imaginea generată
        self.ax_generated = self.fig.add_subplot(gs[0, 1])
        self.ax_generated.set_title('Imaginea Generată')
        self.ax_generated.axis('off')
        
        # Subplot 3: Grafic fitness
        self.ax_fitness = self.fig.add_subplot(gs[0, 2])
        self.ax_fitness.set_title('Evoluția Fitness-ului')
        self.ax_fitness.set_xlabel('Iterații')
        self.ax_fitness.set_ylabel('RMSE (Eroare)')
        self.ax_fitness.grid(True, alpha=0.3)
        
        # Date pentru grafic
        self.iterations = []
        self.fitness_values = []
        self.line, = self.ax_fitness.plot([], [], 'b-', linewidth=2)
        
        # Imaginea afișată
        self.img_display = None
        
        plt.tight_layout()
        plt.ion()  # Mod interactiv
        plt.show()
    
    def update(self, data: dict):
        """
        Actualizează afișajul cu noile date.
        
        Args:
            data: Dicționar cu informații despre progres
                - iteration/generation: Numărul iterației
                - fitness: Valoarea fitness-ului
                - solution: Soluția curentă
                - accuracy: Acuratețea (opțional)
        """
        # Extragem datele
        iteration = data.get('iteration', data.get('generation', 0))
        fitness = data['fitness']
        solution = data['solution']
        accuracy = data.get('accuracy', 0)
        
        # Actualizăm lista de fitness
        self.iterations.append(iteration)
        self.fitness_values.append(fitness)
        
        # Actualizăm imaginea generată
        generated_image = render_solution(solution)
        
        if self.img_display is None:
            self.img_display = self.ax_generated.imshow(generated_image)
        else:
            self.img_display.set_data(generated_image)
        
        self.ax_generated.set_title(
            f'Generată (Acuratețe: {accuracy:.2f}%)\nRMSE: {fitness:.2f}'
        )
        
        # Actualizăm graficul fitness
        self.line.set_data(self.iterations, self.fitness_values)
        self.ax_fitness.relim()
        self.ax_fitness.autoscale_view()
        
        # Redare
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def close(self):
        """Închide fereastra."""
        plt.ioff()
        plt.close(self.fig)
    
    def save(self, filename: str):
        """Salvează figura curentă."""
        self.fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"📊 Grafic salvat: {filename}")
