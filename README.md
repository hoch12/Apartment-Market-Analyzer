# Apartment Market Analyzer

Apartment Market Analyzer je desktopová aplikace napájená strojovým učením, která odhaduje tržní cenu bytů v České republice a předpovídá vývoj jejich hodnoty v čase (10 let).

## 📌 Funkce
- **Odhad tržní ceny**: Predikce ceny na základě lokality (kraje), dispozice (1+kk až 5+1) a užitné plochy.
- **Projekce budoucí hodnoty**: Vizualizace očekávaného růstu hodnoty nemovitosti v horizontu deseti let.
- **Data-Driven**: Aplikace využívá data scrapovaná přímo z realitních portálů.
- **Moderní GUI**: Přehledné rozhraní v češtině postavené na knihovně Tkinter.

---

## 📂 Struktura projektu

```
Car-Market-Analyzer/
├── data/                  # Uložiště dat
│   └── raw/               # Nespracovaná data z webu
├── docs/                  # Detailní dokumentace a analýzy
├── src/
│   ├── app/
│   │   └── gui_app.py     # Hlavní vstupní bod GUI aplikace
│   ├── model/
│   │   ├── inference.py   # Logika predikce a interní API
│   │   ├── train_model.py # Skript pro trénování modelu
│   │   └── *.pkl          # Artefakty natrénovaného modelu
│   └── scraper/
│       └── reality_scraper.py # Modul pro web scraping realit
├── requirements.txt       # Závislosti projektu
└── README.md              # Hlavní dokumentace
```

---

## 🛠️ Technologie

- **`scikit-learn`**: Trénování modelu Random Forest Regressor.
- **`pandas`**: Manipulace a čištění dat.
- **`matplotlib`**: Vizualizace trendů vývoje cen.
- **`selenium`**: Scraping dynamického obsahu z realitních webů.
- **`tkinter`**: Rozhraní aplikace.

---

## 🚀 Jak spustit

### 1. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 2. Sběr dat (Volitelné)
Pokud chcete aktualizovat dataset:
```bash
python src/scraper/reality_scraper.py
```

### 3. Trénování modelu
Po získání dat je nutné model natrénovat:
```bash
python src/model/train_model.py
```

### 4. Spuštění aplikace
```bash
python src/app/gui_app.py
```
