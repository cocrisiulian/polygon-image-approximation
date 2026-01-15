"""
Funcția de fitness (cost) - Calculează diferența dintre imaginea generată și cea originală.
Student A - Componenta critică pentru performanță
"""
import numpy as np
from PIL import Image


def calculate_fitness(generated_image: Image.Image, target_image: Image.Image) -> float:
    """
    Calculează eroarea RMSE (Root Mean Square Error) între două imagini.
    
    RMSE = sqrt( sum((pixel_generated - pixel_target)^2) / num_pixels )
    
    Cu cât RMSE este mai mic, cu atât imaginea generată seamănă mai mult cu cea originală.
    
    Args:
        generated_image: Imaginea generată de poligoane
        target_image: Imaginea țintă originală
    
    Returns:
        float: Valoarea RMSE (0 = perfect, valori mari = diferențe mari)
    """
    # Convertim imaginile la arrays NumPy pentru calcul rapid
    gen_array = np.array(generated_image, dtype=np.float32)
    target_array = np.array(target_image, dtype=np.float32)
    
    # Calculăm diferențele pixel cu pixel
    diff = gen_array - target_array
    
    # RMSE = rădăcina pătrată a mediei pătratelor diferențelor
    mse = np.mean(diff ** 2)
    rmse = np.sqrt(mse)
    
    return rmse


def calculate_pixel_accuracy(generated_image: Image.Image, target_image: Image.Image) -> float:
    """
    Calculează acuratețea procentuală (pentru raportare).
    
    Returns:
        float: Procentul de similaritate (0-100%)
    """
    rmse = calculate_fitness(generated_image, target_image)
    
    # Normalizăm RMSE-ul la un procent (255 = maxim posibil pentru RGB)
    max_error = 255.0
    accuracy = max(0, 100 * (1 - rmse / max_error))
    
    return accuracy


def calculate_fitness_batch(generated_images: list, target_image: Image.Image) -> list:
    """
    Calculează fitness-ul pentru mai multe imagini simultan (pentru GA - populația).
    
    Args:
        generated_images: Lista de imagini generate
        target_image: Imaginea țintă
    
    Returns:
        list: Lista de valori RMSE
    """
    return [calculate_fitness(img, target_image) for img in generated_images]
