"""
Punct de intrare principal pentru proiectul de aproximare a imaginilor.
Permite rularea și compararea algoritmilor SA și GA.

Utilizare:
    python main.py --algorithm sa --image images/test.jpg --polygons 50
    python main.py --algorithm ga --image images/test.jpg --polygons 50
    python main.py --algorithm both --image images/test.jpg --polygons 50
"""

import argparse
import os
import sys
from PIL import Image

# Importăm componentele proiectului
from src.algorithms import SimulatedAnnealing, GeneticAlgorithm
from src.visualization import LiveDisplay, ComparisonAnalyzer
from src.core import render_solution


def prepare_image(image_path: str, max_size: int = 200) -> Image.Image:
    """
    Pregătește imaginea pentru procesare (redimensionare pentru viteză).
    
    Args:
        image_path: Calea către imagine
        max_size: Dimensiunea maximă (lățime/înălțime)
    
    Returns:
        Image.Image: Imaginea pregătită
    """
    print(f"📷 Încărcare imagine: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Eroare: Fișierul {image_path} nu există!")
        sys.exit(1)
    
    img = Image.open(image_path).convert('RGB')
    
    # Redimensionăm pentru performanță
    width, height = img.size
    if width > max_size or height > max_size:
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"   Redimensionat: {width}x{height} → {img.size[0]}x{img.size[1]}")
    else:
        print(f"   Dimensiune: {width}x{height}")
    
    return img


def run_simulated_annealing(target_image: Image.Image, args) -> tuple:
    """
    Rulează Simulated Annealing.
    
    Args:
        target_image: Imaginea țintă
        args: Argumentele din linia de comandă
    
    Returns:
        tuple: (solution, history)
    """
    print("\n🔥 Pornire Simulated Annealing...")
    
    # Callback pentru afișare live (opțional)
    display = None
    if args.live_display:
        display = LiveDisplay(target_image, "Simulated Annealing")
    
    # Creăm și rulăm algoritmul
    sa = SimulatedAnnealing(
        target_image=target_image,
        num_polygons=args.polygons,
        initial_temperature=args.sa_temp,
        cooling_rate=args.sa_cooling,
        max_iterations=args.sa_iterations,
        callback=display.update if display else None
    )
    
    best_solution = sa.run()
    history = sa.get_history()
    
    if display:
        display.save(f"{args.output_dir}/sa_progress.png")
        display.close()
    
    return best_solution, history


def run_genetic_algorithm(target_image: Image.Image, args) -> tuple:
    """
    Rulează Genetic Algorithm.
    
    Args:
        target_image: Imaginea țintă
        args: Argumentele din linia de comandă
    
    Returns:
        tuple: (solution, history)
    """
    print("\n🧬 Pornire Genetic Algorithm...")
    
    # Callback pentru afișare live (opțional)
    display = None
    if args.live_display:
        display = LiveDisplay(target_image, "Genetic Algorithm")
    
    # Creăm și rulăm algoritmul
    ga = GeneticAlgorithm(
        target_image=target_image,
        num_polygons=args.polygons,
        population_size=args.ga_population,
        num_generations=args.ga_generations,
        mutation_rate=args.ga_mutation,
        crossover_rate=args.ga_crossover,
        callback=display.update if display else None
    )
    
    best_solution = ga.run()
    history = ga.get_history()
    
    if display:
        display.save(f"{args.output_dir}/ga_progress.png")
        display.close()
    
    return best_solution, history


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Aproximarea Imaginilor folosind Poligoane - Comparație SA vs GA"
    )
    
    # Argumente generale
    parser.add_argument('--image', type=str, required=True,
                        help='Calea către imaginea țintă')
    parser.add_argument('--algorithm', type=str, choices=['sa', 'ga', 'both'], default='both',
                        help='Algoritmul de rulat: sa, ga sau both')
    parser.add_argument('--polygons', type=int, default=50,
                        help='Numărul de poligoane (default: 50)')
    parser.add_argument('--image-size', type=int, default=200,
                        help='Dimensiunea maximă a imaginii în pixeli (default: 200)')
    parser.add_argument('--output-dir', type=str, default='results',
                        help='Directorul pentru rezultate (default: results)')
    parser.add_argument('--live-display', action='store_true',
                        help='Afișează progresul în timp real')
    
    # Parametrii Simulated Annealing
    parser.add_argument('--sa-temp', type=float, default=100.0,
                        help='Temperatura inițială SA (default: 100.0)')
    parser.add_argument('--sa-cooling', type=float, default=0.995,
                        help='Rata de răcire SA (default: 0.995)')
    parser.add_argument('--sa-iterations', type=int, default=10000,
                        help='Numărul de iterații SA (default: 10000)')
    
    # Parametrii Genetic Algorithm
    parser.add_argument('--ga-population', type=int, default=20,
                        help='Mărimea populației GA (default: 20)')
    parser.add_argument('--ga-generations', type=int, default=1000,
                        help='Numărul de generații GA (default: 1000)')
    parser.add_argument('--ga-mutation', type=float, default=0.1,
                        help='Rata de mutație GA (default: 0.1)')
    parser.add_argument('--ga-crossover', type=float, default=0.7,
                        help='Rata de crossover GA (default: 0.7)')
    
    args = parser.parse_args()
    
    # Creăm directorul de output
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Banner
    print("\n" + "="*70)
    print(" " * 10 + "🎨 APROXIMAREA IMAGINILOR FOLOSIND POLIGOANE 🎨")
    print(" " * 15 + "Analiză Comparativă: SA vs GA")
    print("="*70)
    
    # Pregătim imaginea
    target_image = prepare_image(args.image, args.image_size)
    target_image.save(f"{args.output_dir}/original.png")
    
    # Analizor pentru comparații
    analyzer = ComparisonAnalyzer()
    
    # Rulăm algoritmii
    if args.algorithm in ['sa', 'both']:
        sa_solution, sa_history = run_simulated_annealing(target_image, args)
        analyzer.add_result('SA', sa_history, sa_solution, target_image)
        
        # Salvăm rezultatul SA
        sa_image = render_solution(sa_solution)
        sa_image.save(f"{args.output_dir}/sa_final.png")
    
    if args.algorithm in ['ga', 'both']:
        ga_solution, ga_history = run_genetic_algorithm(target_image, args)
        analyzer.add_result('GA', ga_history, ga_solution, target_image)
        
        # Salvăm rezultatul GA
        ga_image = render_solution(ga_solution)
        ga_image.save(f"{args.output_dir}/ga_final.png")
    
    # Generăm raportul comparativ
    if args.algorithm == 'both':
        print("\n📊 Generare raport comparativ...")
        analyzer.generate_comparison_report(f"{args.output_dir}/comparison_report.png")
        analyzer.generate_summary_table()
        analyzer.save_final_images(args.output_dir)
    
    print("\n✅ Procesare completă!")
    print(f"📁 Rezultate salvate în: {args.output_dir}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
