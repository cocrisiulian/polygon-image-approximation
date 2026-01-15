# 🎨 Aproximarea Imaginilor folosind Poligoane

**Analiză Comparativă: Algoritm Genetic vs Simulated Annealing**

## 📋 Descriere Proiect

Acest proiect reconstruiește imagini raster complexe folosind un set limitat de poligoane semitransparente, comparând performanța a două metaheuristici:

- **🔥 Simulated Annealing (SA)** - căutare locală bazată pe fizică statistică
- **🧬 Algoritm Genetic (GA)** - căutare bazată pe evoluție biologică

**Caracteristici:**

- ✨ **Interfață Grafică (GUI)** - selectare imagine, configurare parametri, export automat
- 📊 **Export Excel** - rapoarte detaliate cu 3 foi de calcul
- ⚡ **Execuție Paralelă** - rulare simultană SA + GA fără interferență
- 🖼️ **Imagini Predefinite** - include Mona Lisa pentru testare rapidă
- 📈 **Vizualizare Live** - progres în timp real (opțional)

## 🚀 Instalare

### Pas 1: Clonează repository-ul

```bash
git clone <repository-url>
cd polygon-image-approximation
```

### Pas 2: Instalează dependențele

```bash
pip install -r requirements.txt
```

**Dependențe:**

- `numpy>=1.24.0` - calcule numerice
- `Pillow>=10.0.0` - procesare imagini
- `matplotlib>=3.7.0` - grafice
- `tqdm>=4.65.0` - progress bars
- `openpyxl>=3.1.0` - export Excel

## 💻 Utilizare

### 🖥️ Mod Grafic (Recomandat)

Lansează interfața grafică:

```bash
python gui_main.py
```

**Pași în GUI:**

1. **Selectează imaginea:**
   - Click "📂 Browse..." pentru imagine proprie
   - Click "🖼️ Mona Lisa" pentru imaginea predefinită
2. **Alege algoritmul:**
   - 🔥 Simulated Annealing (SA)
   - 🧬 Genetic Algorithm (GA)
   - ⚡ Ambii (în paralel) - **recomandat pentru comparație**
3. **Configurează parametrii:**
   - Număr poligoane (10-200)
   - Parametri SA: temperatură, rată răcire, iterații
   - Parametri GA: populație, generații, rată mutație
4. **Click "▶️ START PROCESARE"**
5. **Rezultate:**
   - Excel: `results/raport_comparative.xlsx`
   - Imagini: `results/SA_final.png`, `results/GA_final.png`

### 🖥️ Mod Linie de Comandă

#### Rulare Simulated Annealing

```bash
python main.py --algorithm sa --image images/mona_lisa.jpg --polygons 50 --iterations 10000
```

#### Rulare Algoritm Genetic

```bash
python main.py --algorithm ga --image images/mona_lisa.jpg --polygons 50 --generations 1000 --population 20
```

#### Comparare Ambii Algoritmi

```bash
python main.py --algorithm both --image images/mona_lisa.jpg --polygons 50
```

### 🎯 Exemple Rapide

#### Test rapid cu imagine simplă

```bash
python create_test_images.py
python gui_main.py
```

#### Comparare completă Mona Lisa

```bash
python main.py --algorithm both --image images/mona_lisa.jpg --polygons 30
```

## 📂 Structura Proiect

```
polygon-image-approximation/
├── gui_main.py                 # 🖥️ Interfață grafică (GUI)
├── main.py                     # 🖥️ Interfață linie de comandă (CLI)
├── src/
│   ├── core/
│   │   ├── polygon.py          # Reprezentarea poligoanelor
│   │   ├── fitness.py          # Funcția de cost (RMSE)
│   │   └── renderer.py         # Desenarea poligoanelor
│   ├── algorithms/
│   │   ├── simulated_annealing.py  # 🔥 SA Implementation
│   │   └── genetic_algorithm.py    # 🧬 GA Implementation
│   ├── visualization/
│   │   ├── live_display.py     # Afișare în timp real
│   │   └── analysis.py         # Grafice comparative
│   └── utils/
│       └── excel_exporter.py   # 📊 Export rapoarte Excel
├── images/
│   ├── mona_lisa.jpg           # 🖼️ Imagine predefinită
│   ├── test_simple.png         # Imagine test simplă
│   └── test_gradient.png       # Gradient test
└── results/                    # 📁 Rezultate generate
    ├── raport_comparative.xlsx # 📊 Raport Excel (3 foi)
    ├── SA_final.png            # Rezultat SA
    ├── GA_final.png            # Rezultat GA
    └── comparison_report.png   # Grafice comparative

```

## 📊 Raport Excel (3 Foi de Calcul)

### Foaia 1: Rezultate Generale

- Comparație SA vs GA
- Metrici: Acuratețe (%), RMSE, Timp (secunde)
- Câștigător pe fiecare metrică

### Foaia 2: Detalii Simulated Annealing

- Parametri algoritm (temperatură, rată răcire, etc.)
- Istoric iterații complete:
  - Iterație | Fitness | Temperatură | Rate Acceptare | Acuratețe

### Foaia 3: Detalii Genetic Algorithm

- Parametri algoritm (populație, generații, etc.)
- Istoric generații complete:
  - Generație | Best Fitness | Avg Fitness | Diversitate | Acuratețe

## ⚙️ Parametri Recomandați

### 🔥 Simulated Annealing

- **Temperatură inițială:** 100.0
- **Rată răcire:** 0.995
- **Iterații maxime:** 10000
- **Performanță:** Rapid (~15-25 secunde)
- **Acuratețe:** 65-70%

### 🧬 Genetic Algorithm

- **Populație:** 20
- **Generații:** 1000
- **Rată mutație:** 0.1
- **Rată crossover:** 0.7
- **Performanță:** Lent (~250 secunde)
- **Acuratețe:** 80-85%

## 🎯 Rezultate Așteptate

- **SA:** Mai rapid, acuratețe medie (~67%)
- **GA:** Mai lent, acuratețe superioară (~82%)
- **Concluzie:** GA = mai precis, SA = mai eficient temporal

## 🛠️ Depanare

### Python nu este recunoscut

```bash
# Adaugă Python în PATH (Windows PowerShell)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\<USER>\AppData\Local\Programs\Python\Python314", [EnvironmentVariableTarget]::User)
```

### Lipsesc dependențe

```bash
pip install -r requirements.txt
```

### Erori la import

```bash
# Verifică că ești în directorul proiectului
cd polygon-image-approximation
python gui_main.py
```
