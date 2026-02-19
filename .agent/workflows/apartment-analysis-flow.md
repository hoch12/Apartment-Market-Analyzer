---
description: Kompletní postup pro analýzu trhu s byty
---

Postupujte podle těchto kroků pro sběr dat, trénování modelu a spuštění aplikace:

### 1. Sběr dat (Scraping)
Prvním krokem je získání aktuálních dat o bytech z portálu iDnes Reality.
- V kořenovém adresáři spusťte scraper:
  ```bash
  python src/scraper/reality_scraper.py
  ```
- **Poznámka**: Program otevře prohlížeč. Pokud se objeví okno pro souhlas s cookies, klikněte na "Souhlasím" a pak v terminálu stiskněte **ENTER**.
- Po stažení dat se vytvoří soubor `data/raw/apartments_raw_data.csv`.

### 2. Trénování modelu
Jakmile máte stažená data, musíte natrénovat Machine Learning model.
- Spusťte trénovací skript:
  ```bash
  python src/model/train_model.py
  ```
- Skript vyčistí data, extrahuje parametry (m2, dispozice) a uloží model jako `apartment_price_model.pkl`.

### 3. Spuštění GUI aplikace
Nyní můžete spustit samotnou aplikaci a otestovat odhady cen.
- Spusťte aplikaci:
  ```bash
  python src/app/gui_app.py
  ```
- V aplikaci vyberte kraj, dispozici a zadejte plochu bytu. Klikněte na "ANALYZOVAT TRŽNÍ CENU".

---
**Tip**: Pokud chcete stáhnout více dat, můžete v souboru `config.json` zvýšit hodnotu `num_pages` (aktuálně nastaveno na 50).
