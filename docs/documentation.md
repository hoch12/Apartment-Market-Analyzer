# Apartment Market Analyzer - Uživatelský Manuál v1.0

**Apartment Market Analyzer** je desktopová aplikace pro analýzu realitního trhu v České republice. Slouží k odhadu tržní ceny bytů a predikci budoucího vývoje jejich hodnoty pomocí strojového učení.

## 🚀 Rychlý Start

### Požadavky
- Python 3.8 nebo novější
- Google Chrome (pro stahování dat)

### Instalace
1. Naklonujte repozitář (nebo stáhněte ZIP).
2. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

### Spuštění Aplikace
Pro spuštění grafického rozhraní:
```bash
python src/app/gui_app.py
```

## 🛠 Funkce a Použití

### 1. Odhad Ceny
V hlavním okně aplikace vyplňte:
- **Kraj**: Lokalita, kde se byt nachází.
- **Dispozice**: Typ bytu (např. 2+kk, 3+1).
- **Plocha**: Užitná plocha v metrech čtverečních.

Klikněte na **ANALYZOVAT TRŽNÍ CENU**. Aplikace zobrazí:
- Odhadovanou aktuální tržní cenu.
- Graf predikce vývoje hodnoty na 10 let dopředu.

> **Inteligentní Validace**: Aplikace vás upozorní, pokud zadáte nesmyslnou kombinaci (např. 6+kk o velikosti 20 m²).

### 2. Stahování Dat (Scraping)
Pokud chcete aktualizovat databázi inzerátů z reality.idnes.cz:
```bash
python src/scraper/reality_scraper.py
```
- Skript otevře prohlížeč.
- **DŮLEŽITÉ**: Musíte ručně potvrdit cookies v prohlížeči a stisknout ENTER v terminálu.
- Data se uloží do `data/raw/apartments_raw_data.csv`.

### 3. Trénování Modelu
Po stažení nových dat můžete pře-trénovat model pro vyšší přesnost:
```bash
python src/model/train_model.py
```
- Model se uloží do `src/model/apartment_price_model.pkl`.

### 4. Analýza v Notebooku
Pro detailní průzkum dat (grafy, statistiky) využijte Jupyter Notebook:
- Otevřete soubor `notebooks/Apartment_Price_Analysis.ipynb` ve VS Code nebo Jupyter Lab.

## 🧠 Jak to funguje?

### Data
Aplikace využívá data z tisíců inzerátů, která obsahují informace o:
- Ceně
- Dispozici (1+kk až 6+kk)
- Výměře (m²)
- Lokalitě (kraj/město)

### Model Strojového Učení
Používáme algoritmus **Random Forest Regressor**, který se učí vztahy mezi těmito parametry.
- **Validace**: Data mimo logické meze (např. extrémně levné byty) jsou při trénování ignorována.
- **Lokalita**: Města jsou automaticky mapována do příslušných krajů pro lepší generalizaci.

## ⚠️ Známá Omezení
- Predikce pro velmi specifické lokality (malé vesnice) může být méně přesná než pro velká města.
- Odhad budoucího vývoje je matematická projekce s fixním růstem (4 % ročně) a nezohledňuje makroekonomické šoky.

---
*Verze 1.0.0 | © 2026 Apartment Market Analyzer Team*
