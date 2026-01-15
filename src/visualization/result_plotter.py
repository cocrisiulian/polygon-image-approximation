"""
Modul pentru afișarea graficelor rezultatelor.
Creează ferestre separate cu grafice conform algoritmului rulat.
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import numpy as np
from typing import Optional, Dict, List


class ResultPlotter:
    """Afișează grafice comparative pentru rezultatele algoritmilor."""
    
    def __init__(self):
        """Inițializează plotterul."""
        self.fig = None
    
    def plot_results(self, 
                    target_image: Image.Image,
                    sa_results: Optional[Dict] = None,
                    ga_results: Optional[Dict] = None,
                    save_path: str = "results/grafice_finale.png"):
        """
        Afișează graficele conform algoritmilor rulați.
        
        Args:
            target_image: Imaginea originală
            sa_results: Rezultate SA (None dacă nu a rulat)
            ga_results: Rezultate GA (None dacă nu a rulat)
            save_path: Calea unde să salveze graficul
        """
        if sa_results and ga_results:
            self._plot_both(target_image, sa_results, ga_results, save_path)
        elif sa_results:
            self._plot_sa_only(target_image, sa_results, save_path)
        elif ga_results:
            self._plot_ga_only(target_image, ga_results, save_path)
    
    def _plot_sa_only(self, target_image: Image.Image, sa_results: Dict, save_path: str):
        """Afișează doar graficele SA."""
        self.fig = plt.figure(figsize=(15, 8))
        self.fig.suptitle('🔥 Simulated Annealing - Rezultate', fontsize=16, fontweight='bold')
        
        gs = gridspec.GridSpec(2, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # Row 1: Imagini
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.imshow(target_image)
        ax1.set_title('Imagine Originală', fontweight='bold')
        ax1.axis('off')
        
        ax2 = self.fig.add_subplot(gs[0, 1])
        sa_img = Image.open('results/SA_final.png')
        ax2.imshow(sa_img)
        accuracy = 100 - sa_results.get('fitness_final', 0)
        ax2.set_title(f'Rezultat SA\nAcuratețe: {accuracy:.2f}%', fontweight='bold')
        ax2.axis('off')
        
        # Statistici
        ax3 = self.fig.add_subplot(gs[0, 2])
        ax3.axis('off')
        stats_text = self._format_sa_stats(sa_results)
        ax3.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax3.set_title('📊 Statistici', fontweight='bold')
        
        # Row 2: Grafice evoluție
        history = sa_results.get('history', [])
        
        if history:
            # Fitness evolution
            ax4 = self.fig.add_subplot(gs[1, 0])
            iterations = [h['iteration'] for h in history]
            fitness_vals = [h['fitness'] for h in history]
            ax4.plot(iterations, fitness_vals, 'b-', linewidth=2, label='Fitness (RMSE)')
            ax4.set_xlabel('Iterație')
            ax4.set_ylabel('Fitness (RMSE)')
            ax4.set_title('Evoluția Fitness', fontweight='bold')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
            
            # Temperature evolution
            ax5 = self.fig.add_subplot(gs[1, 1])
            temp_vals = [h['temperature'] for h in history]
            ax5.plot(iterations, temp_vals, 'r-', linewidth=2, label='Temperatură')
            ax5.set_xlabel('Iterație')
            ax5.set_ylabel('Temperatură')
            ax5.set_title('Evoluția Temperaturii', fontweight='bold')
            ax5.grid(True, alpha=0.3)
            ax5.legend()
            
            # Acceptance rate
            ax6 = self.fig.add_subplot(gs[1, 2])
            accept_vals = [h['acceptance_rate'] * 100 for h in history]
            ax6.plot(iterations, accept_vals, 'g-', linewidth=2, label='Rată Acceptare')
            ax6.set_xlabel('Iterație')
            ax6.set_ylabel('Rată Acceptare (%)')
            ax6.set_title('Evoluția Ratei de Acceptare', fontweight='bold')
            ax6.grid(True, alpha=0.3)
            ax6.legend()
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show(block=False)
        plt.pause(0.1)
    
    def _plot_ga_only(self, target_image: Image.Image, ga_results: Dict, save_path: str):
        """Afișează doar graficele GA."""
        self.fig = plt.figure(figsize=(15, 8))
        self.fig.suptitle('🧬 Genetic Algorithm - Rezultate', fontsize=16, fontweight='bold')
        
        gs = gridspec.GridSpec(2, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # Row 1: Imagini
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.imshow(target_image)
        ax1.set_title('Imagine Originală', fontweight='bold')
        ax1.axis('off')
        
        ax2 = self.fig.add_subplot(gs[0, 1])
        ga_img = Image.open('results/GA_final.png')
        ax2.imshow(ga_img)
        accuracy = 100 - ga_results.get('fitness_final', 0)
        ax2.set_title(f'Rezultat GA\nAcuratețe: {accuracy:.2f}%', fontweight='bold')
        ax2.axis('off')
        
        # Statistici
        ax3 = self.fig.add_subplot(gs[0, 2])
        ax3.axis('off')
        stats_text = self._format_ga_stats(ga_results)
        ax3.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax3.set_title('📊 Statistici', fontweight='bold')
        
        # Row 2: Grafice evoluție
        history = ga_results.get('history', [])
        
        if history:
            # Fitness evolution
            ax4 = self.fig.add_subplot(gs[1, 0])
            generations = [h['generation'] for h in history]
            best_fitness = [h['best_fitness'] for h in history]
            avg_fitness = [h['avg_fitness'] for h in history]
            ax4.plot(generations, best_fitness, 'b-', linewidth=2, label='Best Fitness')
            ax4.plot(generations, avg_fitness, 'c--', linewidth=1.5, label='Avg Fitness', alpha=0.7)
            ax4.set_xlabel('Generație')
            ax4.set_ylabel('Fitness (RMSE)')
            ax4.set_title('Evoluția Fitness', fontweight='bold')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
            
            # Diversity evolution
            ax5 = self.fig.add_subplot(gs[1, 1])
            diversity_vals = [h['diversity'] for h in history]
            ax5.plot(generations, diversity_vals, 'm-', linewidth=2, label='Diversitate')
            ax5.set_xlabel('Generație')
            ax5.set_ylabel('Diversitate')
            ax5.set_title('Evoluția Diversității', fontweight='bold')
            ax5.grid(True, alpha=0.3)
            ax5.legend()
            
            # Accuracy evolution
            ax6 = self.fig.add_subplot(gs[1, 2])
            accuracy_vals = [100 - h['best_fitness'] for h in history]
            ax6.plot(generations, accuracy_vals, 'g-', linewidth=2, label='Acuratețe')
            ax6.set_xlabel('Generație')
            ax6.set_ylabel('Acuratețe (%)')
            ax6.set_title('Evoluția Acurateței', fontweight='bold')
            ax6.grid(True, alpha=0.3)
            ax6.legend()
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show(block=False)
        plt.pause(0.1)
    
    def _plot_both(self, target_image: Image.Image, sa_results: Dict, ga_results: Dict, save_path: str):
        """Afișează grafice comparative SA vs GA."""
        self.fig = plt.figure(figsize=(18, 10))
        self.fig.suptitle('⚡ Comparație SA vs GA - Rezultate', fontsize=18, fontweight='bold')
        
        gs = gridspec.GridSpec(3, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # Row 1: Imagini
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.imshow(target_image)
        ax1.set_title('Imagine Originală', fontweight='bold', fontsize=12)
        ax1.axis('off')
        
        ax2 = self.fig.add_subplot(gs[0, 1])
        sa_img = Image.open('results/SA_final.png')
        ax2.imshow(sa_img)
        sa_accuracy = 100 - sa_results.get('fitness_final', 0)
        ax2.set_title(f'🔥 Rezultat SA\nAcuratețe: {sa_accuracy:.2f}%', fontweight='bold', fontsize=12)
        ax2.axis('off')
        
        ax3 = self.fig.add_subplot(gs[0, 2])
        ga_img = Image.open('results/GA_final.png')
        ax3.imshow(ga_img)
        ga_accuracy = 100 - ga_results.get('fitness_final', 0)
        ax3.set_title(f'🧬 Rezultat GA\nAcuratețe: {ga_accuracy:.2f}%', fontweight='bold', fontsize=12)
        ax3.axis('off')
        
        # Row 2: Evoluția Fitness
        sa_history = sa_results.get('history', [])
        ga_history = ga_results.get('history', [])
        
        # SA Fitness
        ax4 = self.fig.add_subplot(gs[1, 0])
        if sa_history:
            iterations = [h['iteration'] for h in sa_history]
            fitness_vals = [h['fitness'] for h in sa_history]
            ax4.plot(iterations, fitness_vals, 'b-', linewidth=2, label='SA Fitness')
        ax4.set_xlabel('Iterație')
        ax4.set_ylabel('Fitness (RMSE)')
        ax4.set_title('🔥 SA - Evoluția Fitness', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        # GA Fitness
        ax5 = self.fig.add_subplot(gs[1, 1])
        if ga_history:
            generations = [h['generation'] for h in ga_history]
            best_fitness = [h['best_fitness'] for h in ga_history]
            avg_fitness = [h['avg_fitness'] for h in ga_history]
            ax5.plot(generations, best_fitness, 'g-', linewidth=2, label='Best')
            ax5.plot(generations, avg_fitness, 'c--', linewidth=1.5, label='Avg', alpha=0.7)
        ax5.set_xlabel('Generație')
        ax5.set_ylabel('Fitness (RMSE)')
        ax5.set_title('🧬 GA - Evoluția Fitness', fontweight='bold')
        ax5.grid(True, alpha=0.3)
        ax5.legend()
        
        # Comparație directă
        ax6 = self.fig.add_subplot(gs[1, 2])
        if sa_history and ga_history:
            # Normalizăm la același număr de puncte
            sa_points = min(len(sa_history), 20)
            ga_points = min(len(ga_history), 20)
            
            sa_step = max(1, len(sa_history) // sa_points)
            ga_step = max(1, len(ga_history) // ga_points)
            
            sa_x = list(range(sa_points))
            sa_y = [sa_history[i * sa_step]['fitness'] for i in range(sa_points)]
            
            ga_x = list(range(ga_points))
            ga_y = [ga_history[i * ga_step]['best_fitness'] for i in range(ga_points)]
            
            ax6.plot(sa_x, sa_y, 'b-', linewidth=2, label='SA', marker='o')
            ax6.plot(ga_x, ga_y, 'g-', linewidth=2, label='GA', marker='s')
        ax6.set_xlabel('Progres Normalizat')
        ax6.set_ylabel('Fitness (RMSE)')
        ax6.set_title('⚡ Comparație Directă', fontweight='bold')
        ax6.grid(True, alpha=0.3)
        ax6.legend()
        
        # Row 3: Metrici comparative
        ax7 = self.fig.add_subplot(gs[2, :])
        
        # Tabel comparativ
        metrics = [
            ['Metrică', 'SA', 'GA', 'Câștigător'],
            ['Acuratețe (%)', f'{sa_accuracy:.2f}', f'{ga_accuracy:.2f}', 
             '🧬 GA' if ga_accuracy > sa_accuracy else '🔥 SA'],
            ['RMSE Final', f"{sa_results.get('fitness_final', 0):.2f}", 
             f"{ga_results.get('fitness_final', 0):.2f}",
             '🧬 GA' if ga_results.get('fitness_final', 0) < sa_results.get('fitness_final', 0) else '🔥 SA'],
            ['Timp (sec)', f"{sa_results.get('total_time', 0):.2f}", 
             f"{ga_results.get('total_time', 0):.2f}",
             '🔥 SA' if sa_results.get('total_time', 0) < ga_results.get('total_time', 0) else '🧬 GA'],
        ]
        
        table = ax7.table(cellText=metrics, cellLoc='center', loc='center',
                         colWidths=[0.25, 0.2, 0.2, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Colorează header
        for i in range(4):
            table[(0, i)].set_facecolor('#366092')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        ax7.axis('off')
        ax7.set_title('📊 Tabel Comparativ Final', fontweight='bold', fontsize=14, pad=20)
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show(block=False)
        plt.pause(0.1)
    
    def _format_sa_stats(self, sa_results: Dict) -> str:
        """Formatează statistici SA."""
        return f"""
🔥 SIMULATED ANNEALING

Parametri:
  • Temp. inițială: {sa_results.get('initial_temp', 0):.1f}
  • Rată răcire: {sa_results.get('cooling_rate', 0):.4f}
  • Iterații: {sa_results.get('iterations', 0)}

Rezultate:
  • Fitness final: {sa_results.get('fitness_final', 0):.2f}
  • Acuratețe: {100 - sa_results.get('fitness_final', 0):.2f}%
  • Timp: {sa_results.get('total_time', 0):.2f}s
"""
    
    def _format_ga_stats(self, ga_results: Dict) -> str:
        """Formatează statistici GA."""
        return f"""
🧬 GENETIC ALGORITHM

Parametri:
  • Populație: {ga_results.get('population_size', 0)}
  • Generații: {ga_results.get('generations', 0)}
  • Mutație: {ga_results.get('mutation_rate', 0):.2f}

Rezultate:
  • Fitness final: {ga_results.get('fitness_final', 0):.2f}
  • Acuratețe: {100 - ga_results.get('fitness_final', 0):.2f}%
  • Timp: {ga_results.get('total_time', 0):.2f}s
"""
    
    def close(self):
        """Închide ferestrele de grafice."""
        if self.fig:
            plt.close(self.fig)
