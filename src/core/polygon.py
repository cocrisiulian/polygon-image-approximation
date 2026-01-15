"""
Reprezentarea poligoanelor și a soluțiilor.
Student A - Infrastructură de bază
"""
import random
import copy
from typing import List, Tuple


class Polygon:
    """
    Reprezintă un poligon (triunghi) cu 3 puncte și culoare RGBA.
    
    Atribute:
        points: Lista de 3 tuple (x, y) - coordonatele vârfurilor
        color: Tuple (R, G, B, A) - culoarea cu transparență (0-255)
    """
    
    def __init__(self, width: int, height: int, random_init: bool = True):
        """
        Inițializează un poligon.
        
        Args:
            width: Lățimea imaginii
            height: Înălțimea imaginii
            random_init: Dacă True, generează coordonate și culori aleatorii
        """
        self.width = width
        self.height = height
        
        if random_init:
            # Generăm 3 puncte aleatorii pentru triunghi
            self.points = [
                (random.randint(0, width), random.randint(0, height)),
                (random.randint(0, width), random.randint(0, height)),
                (random.randint(0, width), random.randint(0, height))
            ]
            
            # Culoare RGBA aleatorie (A = opacitate între 30-150 pentru transparență)
            self.color = (
                random.randint(0, 255),  # R
                random.randint(0, 255),  # G
                random.randint(0, 255),  # B
                random.randint(30, 150)  # A (alpha/opacitate)
            )
        else:
            self.points = [(0, 0), (0, 0), (0, 0)]
            self.color = (0, 0, 0, 0)
    
    def mutate(self, mutation_rate: float = 0.1):
        """
        Modifică ușor poligonul (pentru SA sau GA).
        
        Args:
            mutation_rate: Probabilitatea de mutație pentru fiecare componentă
        """
        # Mutație puncte (mișcări mici)
        new_points = []
        for x, y in self.points:
            if random.random() < mutation_rate:
                # Mișcare mică (-20 până la +20 pixeli)
                dx = random.randint(-20, 20)
                dy = random.randint(-20, 20)
                x = max(0, min(self.width, x + dx))
                y = max(0, min(self.height, y + dy))
            new_points.append((x, y))
        self.points = new_points
        
        # Mutație culoare
        if random.random() < mutation_rate:
            r, g, b, a = self.color
            # Schimbare mică de culoare
            r = max(0, min(255, r + random.randint(-30, 30)))
            g = max(0, min(255, g + random.randint(-30, 30)))
            b = max(0, min(255, b + random.randint(-30, 30)))
            a = max(30, min(150, a + random.randint(-20, 20)))
            self.color = (r, g, b, a)
    
    def copy(self) -> 'Polygon':
        """Returnează o copie profundă a poligonului."""
        new_poly = Polygon(self.width, self.height, random_init=False)
        new_poly.points = copy.deepcopy(self.points)
        new_poly.color = self.color
        return new_poly
    
    def __repr__(self):
        return f"Polygon(points={self.points}, color={self.color})"


class Solution:
    """
    Reprezintă o soluție completă: o listă de poligoane.
    Aceasta este structura de date principală pe care o optimizează algoritmii.
    """
    
    def __init__(self, num_polygons: int, width: int, height: int, random_init: bool = True):
        """
        Inițializează o soluție cu un număr specificat de poligoane.
        
        Args:
            num_polygons: Numărul de poligoane din soluție
            width: Lățimea imaginii
            height: Înălțimea imaginii
            random_init: Dacă True, generează poligoane aleatorii
        """
        self.num_polygons = num_polygons
        self.width = width
        self.height = height
        self.fitness_value = float('inf')  # Inițial, fitness-ul este foarte prost
        
        if random_init:
            self.polygons = [Polygon(width, height) for _ in range(num_polygons)]
        else:
            self.polygons = []
    
    def set_fitness(self, fitness: float):
        """Setează valoarea fitness-ului (eroarea)."""
        self.fitness_value = fitness
    
    def get_fitness(self) -> float:
        """Returnează valoarea curentă a fitness-ului."""
        return self.fitness_value
    
    def copy(self) -> 'Solution':
        """Returnează o copie profundă a soluției."""
        new_solution = Solution(self.num_polygons, self.width, self.height, random_init=False)
        new_solution.polygons = [poly.copy() for poly in self.polygons]
        new_solution.fitness_value = self.fitness_value
        return new_solution
    
    def perturb(self, num_changes: int = 1):
        """
        Perturbă soluția modificând un număr mic de poligoane.
        Folosit în Simulated Annealing.
        
        Args:
            num_changes: Câte poligoane să modifice
        """
        for _ in range(num_changes):
            # Alegem un poligon aleatoriu și îl mutăm
            idx = random.randint(0, len(self.polygons) - 1)
            self.polygons[idx].mutate(mutation_rate=0.3)
    
    def __repr__(self):
        return f"Solution({len(self.polygons)} polygons, fitness={self.fitness_value:.2f})"
