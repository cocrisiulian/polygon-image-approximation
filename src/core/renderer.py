"""
Renderer - Desenează poligoanele și generează imaginea.
Student B - Sistemul de vizualizare
"""
from PIL import Image, ImageDraw
from typing import List
from .polygon import Solution, Polygon


def render_solution(solution: Solution, background_color=(255, 255, 255)) -> Image.Image:
    """
    Desenează o soluție (listă de poligoane) ca imagine.
    
    Args:
        solution: Soluția ce conține lista de poligoane
        background_color: Culoarea de fundal (implicit alb)
    
    Returns:
        Image.Image: Imaginea generată
    """
    # Creăm o imagine albă de fundal
    img = Image.new('RGB', (solution.width, solution.height), background_color)
    
    # Desenăm fiecare poligon cu transparență
    for polygon in solution.polygons:
        # Creăm un layer transparent pentru fiecare poligon
        overlay = Image.new('RGBA', (solution.width, solution.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Desenăm triunghiul
        draw.polygon(polygon.points, fill=polygon.color)
        
        # Combinăm layer-ul cu imaginea principală (alpha blending)
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    return img


def render_polygon_outline(solution: Solution) -> Image.Image:
    """
    Desenează doar contururile poligoanelor (pentru debugging).
    
    Args:
        solution: Soluția ce conține lista de poligoane
    
    Returns:
        Image.Image: Imaginea cu contururi
    """
    img = Image.new('RGB', (solution.width, solution.height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    for polygon in solution.polygons:
        # Desenăm doar conturul
        draw.polygon(polygon.points, outline=(0, 0, 0), width=1)
    
    return img


def render_comparison(original: Image.Image, generated: Image.Image, fitness: float) -> Image.Image:
    """
    Creează o imagine comparativă side-by-side.
    
    Args:
        original: Imaginea originală
        generated: Imaginea generată
        fitness: Valoarea fitness-ului
    
    Returns:
        Image.Image: Imagine combinată cu text
    """
    from PIL import ImageFont
    
    width = original.width
    height = original.height
    
    # Creăm canvas dublu
    comparison = Image.new('RGB', (width * 2 + 10, height), (200, 200, 200))
    
    # Lipim imaginile
    comparison.paste(original, (0, 0))
    comparison.paste(generated, (width + 10, 0))
    
    # Adăugăm text cu fitness-ul
    draw = ImageDraw.Draw(comparison)
    text = f"RMSE: {fitness:.2f}"
    
    try:
        # Încercăm să folosim un font
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Dacă nu găsim font, folosim default
        font = ImageFont.load_default()
    
    draw.text((10, 10), "Original", fill=(255, 255, 255), font=font)
    draw.text((width + 20, 10), f"Generated ({text})", fill=(255, 255, 255), font=font)
    
    return comparison
