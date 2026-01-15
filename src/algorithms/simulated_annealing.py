"""
Simulated Annealing Algorithm
Student A - Implementarea algoritmului bazat pe căutare locală

Principiu:
- Începem cu o soluție aleatorie și o "temperatură" mare
- La fiecare iterație, perturbăm soluția
- Dacă noua soluție e mai bună, o acceptăm
- Dacă e mai proastă, o acceptăm cu probabilitate exp(-ΔE/T)
- Temperatura scade treptat (răcire)
"""
import math
import random
import time
from typing import Callable, Optional
from ..core.polygon import Solution
from ..core.fitness import calculate_fitness, calculate_pixel_accuracy
from ..core.renderer import render_solution
from PIL import Image


class SimulatedAnnealing:
    """
    Implementarea algoritmului Simulated Annealing pentru aproximarea imaginilor.
    """
    
    def __init__(
        self,
        target_image: Image.Image,
        num_polygons: int = 50,
        initial_temperature: float = 100.0,
        cooling_rate: float = 0.995,
        min_temperature: float = 0.01,
        max_iterations: int = 10000,
        callback: Optional[Callable] = None
    ):
        """
        Inițializează algoritmul SA.
        
        Args:
            target_image: Imaginea țintă de aproximat
            num_polygons: Numărul de poligoane folosite
            initial_temperature: Temperatura inițială (T0)
            cooling_rate: Rata de răcire (alpha) - temperatura se înmulțește cu aceasta
            min_temperature: Temperatura minimă (criteriu de oprire)
            max_iterations: Numărul maxim de iterații
            callback: Funcție opțională apelată după fiecare iterație
        """
        self.target_image = target_image.convert('RGB')
        self.width, self.height = target_image.size
        self.num_polygons = num_polygons
        
        # Parametrii SA
        self.temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.max_iterations = max_iterations
        
        # Callback pentru vizualizare
        self.callback = callback
        
        # Statistici
        self.history = {
            'fitness': [],
            'temperature': [],
            'acceptance_rate': [],
            'time': []
        }
        
        # Soluția curentă și cea mai bună
        self.current_solution = None
        self.best_solution = None
        self.best_fitness = float('inf')
    
    def _acceptance_probability(self, current_fitness: float, new_fitness: float) -> float:
        """
        Calculează probabilitatea de acceptare a unei soluții mai proaste.
        
        Formula Metropolis: P = exp(-ΔE / T)
        unde ΔE = new_fitness - current_fitness (pozitiv dacă soluția e mai proastă)
        
        Args:
            current_fitness: Fitness-ul soluției curente
            new_fitness: Fitness-ul soluției noi
        
        Returns:
            float: Probabilitatea de acceptare (0-1)
        """
        if new_fitness < current_fitness:
            # Soluție mai bună - acceptăm întotdeauna
            return 1.0
        
        # Soluție mai proastă - acceptăm cu probabilitate scăzută
        delta_e = new_fitness - current_fitness
        probability = math.exp(-delta_e / self.temperature)
        return probability
    
    def run(self) -> Solution:
        """
        Rulează algoritmul Simulated Annealing.
        
        Returns:
            Solution: Cea mai bună soluție găsită
        """
        print(f"\n{'='*60}")
        print(f"🔥 SIMULATED ANNEALING - Start")
        print(f"{'='*60}")
        print(f"Poligoane: {self.num_polygons}")
        print(f"Temperatură inițială: {self.initial_temperature}")
        print(f"Rată de răcire: {self.cooling_rate}")
        print(f"Iterații maxime: {self.max_iterations}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # Inițializăm soluția curentă (aleatorie)
        self.current_solution = Solution(self.num_polygons, self.width, self.height)
        
        # Calculăm fitness-ul inițial
        current_image = render_solution(self.current_solution)
        current_fitness = calculate_fitness(current_image, self.target_image)
        self.current_solution.set_fitness(current_fitness)
        
        # Inițial, soluția curentă e și cea mai bună
        self.best_solution = self.current_solution.copy()
        self.best_fitness = current_fitness
        
        # Contoare pentru statistici
        iterations = 0
        accepted_moves = 0
        rejected_moves = 0
        
        # Bucla principală
        while self.temperature > self.min_temperature and iterations < self.max_iterations:
            iterations += 1
            
            # 1. PERTURBĂM soluția curentă (generăm o soluție vecină)
            neighbor_solution = self.current_solution.copy()
            neighbor_solution.perturb(num_changes=1)
            
            # 2. EVALUĂM soluția vecină
            neighbor_image = render_solution(neighbor_solution)
            neighbor_fitness = calculate_fitness(neighbor_image, self.target_image)
            neighbor_solution.set_fitness(neighbor_fitness)
            
            # 3. DECIDEM dacă acceptăm soluția nouă
            acceptance_prob = self._acceptance_probability(current_fitness, neighbor_fitness)
            
            if random.random() < acceptance_prob:
                # Acceptăm soluția nouă
                self.current_solution = neighbor_solution
                current_fitness = neighbor_fitness
                accepted_moves += 1
                
                # Actualizăm cel mai bun rezultat dacă e cazul
                if neighbor_fitness < self.best_fitness:
                    self.best_solution = neighbor_solution.copy()
                    self.best_fitness = neighbor_fitness
            else:
                rejected_moves += 1
            
            # 4. RĂCIM sistemul (scădem temperatura)
            self.temperature *= self.cooling_rate
            
            # 5. COLECTĂM statistici
            if iterations % 10 == 0:
                elapsed_time = time.time() - start_time
                self.history['fitness'].append(self.best_fitness)
                self.history['temperature'].append(self.temperature)
                acceptance_rate = accepted_moves / (accepted_moves + rejected_moves) if (accepted_moves + rejected_moves) > 0 else 0
                self.history['acceptance_rate'].append(acceptance_rate)
                self.history['time'].append(elapsed_time)
            
            # 6. CALLBACK pentru vizualizare live
            if self.callback and iterations % 50 == 0:
                accuracy = calculate_pixel_accuracy(
                    render_solution(self.best_solution),
                    self.target_image
                )
                self.callback({
                    'iteration': iterations,
                    'fitness': self.best_fitness,
                    'temperature': self.temperature,
                    'accuracy': accuracy,
                    'solution': self.best_solution,
                    'acceptance_rate': acceptance_rate
                })
            
            # 7. AFIȘĂM progresul la consola
            if iterations % 500 == 0:
                accuracy = calculate_pixel_accuracy(
                    render_solution(self.best_solution),
                    self.target_image
                )
                print(f"Iterație {iterations:5d} | "
                      f"Fitness: {self.best_fitness:7.2f} | "
                      f"Temp: {self.temperature:6.2f} | "
                      f"Accept: {acceptance_rate:.2%} | "
                      f"Acuratețe: {accuracy:.2f}%")
        
        # Sfârșitul algoritmului
        total_time = time.time() - start_time
        final_accuracy = calculate_pixel_accuracy(
            render_solution(self.best_solution),
            self.target_image
        )
        
        print(f"\n{'='*60}")
        print(f"✅ SIMULATED ANNEALING - Finalizat")
        print(f"{'='*60}")
        print(f"Iterații totale: {iterations}")
        print(f"Timp total: {total_time:.2f} secunde")
        print(f"Fitness final: {self.best_fitness:.2f}")
        print(f"Acuratețe finală: {final_accuracy:.2f}%")
        print(f"Mutări acceptate: {accepted_moves} ({accepted_moves/iterations:.1%})")
        print(f"Mutări respinse: {rejected_moves} ({rejected_moves/iterations:.1%})")
        print(f"{'='*60}\n")
        
        return self.best_solution
    
    def get_history(self) -> dict:
        """Returnează istoricul pentru analiză."""
        return self.history
