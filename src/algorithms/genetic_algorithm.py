"""
Genetic Algorithm
Student B - Implementarea algoritmului bazat pe evoluție

Principiu:
- Populația = mulțime de soluții (indivizi)
- Selecție: Părinții mai buni au șanse mai mari să se reproducă
- Crossover: Combinarea a doi părinți pentru a crea copii
- Mutație: Modificări aleatorii mici
- Elitism: Păstrăm cei mai buni indivizi
"""
import random
import time
from typing import Callable, Optional, List
from ..core.polygon import Solution
from ..core.fitness import calculate_fitness, calculate_pixel_accuracy
from ..core.renderer import render_solution
from PIL import Image


class GeneticAlgorithm:
    """
    Implementarea algoritmului genetic pentru aproximarea imaginilor.
    """
    
    def __init__(
        self,
        target_image: Image.Image,
        num_polygons: int = 50,
        population_size: int = 20,
        num_generations: int = 1000,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.7,
        elitism_count: int = 2,
        tournament_size: int = 3,
        callback: Optional[Callable] = None
    ):
        """
        Inițializează algoritmul genetic.
        
        Args:
            target_image: Imaginea țintă
            num_polygons: Numărul de poligoane per individ
            population_size: Mărimea populației
            num_generations: Numărul de generații (iterații)
            mutation_rate: Probabilitatea de mutație (0-1)
            crossover_rate: Probabilitatea de încrucișare (0-1)
            elitism_count: Câți cei mai buni indivizi să păstrăm
            tournament_size: Mărimea turneului pentru selecție
            callback: Funcție opțională pentru vizualizare
        """
        self.target_image = target_image.convert('RGB')
        self.width, self.height = target_image.size
        self.num_polygons = num_polygons
        
        # Parametrii GA
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        
        # Callback pentru vizualizare
        self.callback = callback
        
        # Statistici
        self.history = {
            'best_fitness': [],
            'avg_fitness': [],
            'diversity': [],
            'time': []
        }
        
        # Populația
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
    
    def _initialize_population(self):
        """Creează populația inițială cu indivizi aleatorii."""
        print("🧬 Generăm populația inițială...")
        self.population = [
            Solution(self.num_polygons, self.width, self.height)
            for _ in range(self.population_size)
        ]
    
    def _evaluate_population(self):
        """Calculează fitness-ul pentru toți indivizii din populație."""
        for individual in self.population:
            image = render_solution(individual)
            fitness = calculate_fitness(image, self.target_image)
            individual.set_fitness(fitness)
            
            # Actualizăm cel mai bun individ
            if fitness < self.best_fitness:
                self.best_solution = individual.copy()
                self.best_fitness = fitness
    
    def _tournament_selection(self) -> Solution:
        """
        Selecția prin turneu: alegem random K indivizi și returnăm cel mai bun.
        
        Returns:
            Solution: Individul câștigător
        """
        tournament = random.sample(self.population, self.tournament_size)
        winner = min(tournament, key=lambda ind: ind.get_fitness())
        return winner
    
    def _crossover(self, parent1: Solution, parent2: Solution) -> tuple:
        """
        Încrucișare (Crossover) - combină doi părinți pentru a crea doi copii.
        
        Metodă: Single-point crossover pe lista de poligoane
        
        Args:
            parent1: Primul părinte
            parent2: Al doilea părinte
        
        Returns:
            tuple: (child1, child2)
        """
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        if random.random() < self.crossover_rate:
            # Punct de tăiere aleatoriu
            crossover_point = random.randint(1, self.num_polygons - 1)
            
            # Schimbăm poligoanele după punctul de tăiere
            child1.polygons = (
                parent1.polygons[:crossover_point] +
                parent2.polygons[crossover_point:]
            )
            child2.polygons = (
                parent2.polygons[:crossover_point] +
                parent1.polygons[crossover_point:]
            )
        
        return child1, child2
    
    def _mutate(self, individual: Solution):
        """
        Aplică mutații asupra unui individ.
        
        Args:
            individual: Individul de modificat
        """
        for polygon in individual.polygons:
            if random.random() < self.mutation_rate:
                polygon.mutate(mutation_rate=0.3)
    
    def _calculate_diversity(self) -> float:
        """
        Calculează diversitatea populației (cât de diferite sunt soluțiile).
        
        Returns:
            float: Scorul de diversitate
        """
        if len(self.population) < 2:
            return 0.0
        
        # Calculăm variația fitness-urilor
        fitnesses = [ind.get_fitness() for ind in self.population]
        avg_fitness = sum(fitnesses) / len(fitnesses)
        variance = sum((f - avg_fitness) ** 2 for f in fitnesses) / len(fitnesses)
        
        return variance ** 0.5
    
    def run(self) -> Solution:
        """
        Rulează algoritmul genetic.
        
        Returns:
            Solution: Cea mai bună soluție găsită
        """
        print(f"\n{'='*60}")
        print(f"🧬 GENETIC ALGORITHM - Start")
        print(f"{'='*60}")
        print(f"Poligoane: {self.num_polygons}")
        print(f"Populație: {self.population_size}")
        print(f"Generații: {self.num_generations}")
        print(f"Rată mutație: {self.mutation_rate}")
        print(f"Rată crossover: {self.crossover_rate}")
        print(f"Elitism: {self.elitism_count}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # 1. INIȚIALIZĂM populația
        self._initialize_population()
        
        # 2. EVALUĂM populația inițială
        self._evaluate_population()
        
        # 3. EVOLUȚIE (bucla principală)
        for generation in range(self.num_generations):
            # Sortăm populația după fitness (cei mai buni primii)
            self.population.sort(key=lambda ind: ind.get_fitness())
            
            # Creăm noua generație
            new_population = []
            
            # ELITISM: Păstrăm cei mai buni indivizi
            new_population.extend([ind.copy() for ind in self.population[:self.elitism_count]])
            
            # Generăm restul populației prin selecție + crossover + mutație
            while len(new_population) < self.population_size:
                # SELECȚIE: Alegem doi părinți
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()
                
                # CROSSOVER: Creăm doi copii
                child1, child2 = self._crossover(parent1, parent2)
                
                # MUTAȚIE: Aplicăm mutații
                self._mutate(child1)
                self._mutate(child2)
                
                # Adăugăm copiii în noua populație
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            # Înlocuim vechea populație
            self.population = new_population[:self.population_size]
            
            # EVALUĂM noua populație
            self._evaluate_population()
            
            # COLECTĂM statistici
            if generation % 5 == 0:
                elapsed_time = time.time() - start_time
                fitnesses = [ind.get_fitness() for ind in self.population]
                avg_fitness = sum(fitnesses) / len(fitnesses)
                diversity = self._calculate_diversity()
                
                self.history['best_fitness'].append(self.best_fitness)
                self.history['avg_fitness'].append(avg_fitness)
                self.history['diversity'].append(diversity)
                self.history['time'].append(elapsed_time)
            
            # CALLBACK pentru vizualizare
            if self.callback and generation % 10 == 0:
                accuracy = calculate_pixel_accuracy(
                    render_solution(self.best_solution),
                    self.target_image
                )
                self.callback({
                    'generation': generation,
                    'fitness': self.best_fitness,
                    'avg_fitness': avg_fitness,
                    'diversity': diversity,
                    'accuracy': accuracy,
                    'solution': self.best_solution
                })
            
            # AFIȘĂM progresul
            if generation % 50 == 0:
                accuracy = calculate_pixel_accuracy(
                    render_solution(self.best_solution),
                    self.target_image
                )
                print(f"Generație {generation:4d} | "
                      f"Best: {self.best_fitness:7.2f} | "
                      f"Avg: {avg_fitness:7.2f} | "
                      f"Diversitate: {diversity:6.2f} | "
                      f"Acuratețe: {accuracy:.2f}%")
        
        # SFÂRȘITUL algoritmului
        total_time = time.time() - start_time
        final_accuracy = calculate_pixel_accuracy(
            render_solution(self.best_solution),
            self.target_image
        )
        
        print(f"\n{'='*60}")
        print(f"✅ GENETIC ALGORITHM - Finalizat")
        print(f"{'='*60}")
        print(f"Generații totale: {self.num_generations}")
        print(f"Timp total: {total_time:.2f} secunde")
        print(f"Fitness final: {self.best_fitness:.2f}")
        print(f"Acuratețe finală: {final_accuracy:.2f}%")
        print(f"{'='*60}\n")
        
        return self.best_solution
    
    def get_history(self) -> dict:
        """Returnează istoricul pentru analiză."""
        return self.history
