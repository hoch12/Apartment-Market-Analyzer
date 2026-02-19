# Apartment Market Scraper

This module is responsible for collecting real-world apartment listings from **reality.idnes.cz**.

## 🛠️ How It Works

1.  **Exploration**:
    - Targets apartment listings for sale.
    - Extracts: Title (includes disposition and area), Price, and Location.
2.  **Scraping**:
    - Uses Selenium with headless Chrome options.
    - Implements basic debouncing and random delays to mimic human behavior.
3.  **Data Extraction**:
    - Parses attributes from listing title like disposition (1+kk, 2+1...) and size in square meters.
4.  **Persistence**:
    - Appends data to `data/raw/apartments_raw_data.csv`.

## 🚀 How to Run

```bash
python src/scraper/reality_scraper.py
```
