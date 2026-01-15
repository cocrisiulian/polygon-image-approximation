# 🚀 Comenzi Rapide - Reference Sheet

## Setup Inițial

```powershell
# Instalare dependențe
pip install -r requirements.txt

# Verificare proiect
python verify_project.py

# Generare imagini test
python create_test_images.py

# Rulare teste automate
python test_suite.py
```

---

## Rulare Algoritmi

### Simulated Annealing (Rapid - 2 min)

```powershell
python main.py --algorithm sa --image images/test_simple.png --polygons 30 --sa-iterations 5000
```

### Genetic Algorithm (Moderat - 3 min)

```powershell
python main.py --algorithm ga --image images/test_simple.png --polygons 30 --ga-generations 500
```

### Comparație Completă (Recomandat - 5 min)

```powershell
python main.py --algorithm both --image images/test_simple.png --polygons 30
```

---

## Rulare cu Vizualizare Live

```powershell
# SA cu live display
python main.py --algorithm sa --image images/test_simple.png --polygons 30 --live-display

# GA cu live display
python main.py --algorithm ga --image images/test_simple.png --polygons 30 --live-display

# Ambii cu live display (IMPRESIONANT!)
python main.py --algorithm both --image images/test_gradient.png --polygons 40 --live-display
```

---

## Tuning Parametrii

### SA: Explorare Agresivă

```powershell
python main.py --algorithm sa --sa-temp 200 --sa-cooling 0.99 --sa-iterations 20000
```

### SA: Convergență Lentă

```powershell
python main.py --algorithm sa --sa-temp 50 --sa-cooling 0.999 --sa-iterations 30000
```

### GA: Populație Mare

```powershell
python main.py --algorithm ga --ga-population 50 --ga-generations 2000
```

### GA: Mutație Agresivă

```powershell
python main.py --algorithm ga --ga-mutation 0.2 --ga-crossover 0.6
```

---

## Imagini de Diferite Dimensiuni

### Mică (Rapid - Test)

```powershell
python main.py --algorithm both --image test.jpg --image-size 100 --polygons 20
```

### Medie (Standard)

```powershell
python main.py --algorithm both --image test.jpg --image-size 200 --polygons 50
```

### Mare (Calitate)

```powershell
python main.py --algorithm both --image test.jpg --image-size 400 --polygons 100
```

## Troubleshooting

### Eroare: Module not found

```powershell
pip install numpy pillow matplotlib tqdm
```

### Algoritmii sunt prea lenți

```powershell
# Reduceți dimensiunea imaginii
python main.py --image-size 150

# Reduceți numărul de poligoane
python main.py --polygons 30

# Reduceți iterațiile
python main.py --sa-iterations 5000 --ga-generations 500
```
