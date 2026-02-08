# Sauto.cz Web Scraper

This module is responsible for collecting real-world used car data from the Czech marketplace **Sauto.cz**.

## 📌 Inspiration & Origin
The logic for this scraper was inspired by the **Data Collection (CIT)** university course, specifically the project where we developed a crawler for `idnes.cz`.
- **Concept Reuse**: We adapted the principles of DOM traversal and CSS/XPath selectors.
- **Enhancements**: Unlike the static crawler for CIT, this project typically requires **Selenium** to handle the dynamic JavaScript content, "infinite scrolling" lazy loading, and cookie consent banners found on modern e-commerce sites like Sauto.

## 🛠️ How It Works

1.  **Initialization**:
    - Launches a headless (or visible) Chrome browser using `selenium`.
    - Loads configuration from `config.json` (target URL, number of pages).
    - Checks `scraper_state.json` to see if it should resume from a previous run.

2.  **Navigation & Interaction**:
    - Automatically clicks the "Souhlasím" (Agree) button on the cookie banner.
    - Iterates through paginated results (e.g., `?strana=1`, `?strana=2`).
    - **Lazy Loading**: Simulates user scrolling (pressing `PAGE_DOWN`) to trigger the AJAX loading of lower listings.

3.  **Data Extraction**:
    - Selects ad elements using flexible XPath selectors.
    - Extracts:
        - **Title** (Brand/Model)
        - **Price** (Parsed from raw text)
        - **Description** (Year, Mileage, Power, Fuel, Transmission)
        - **URL** (For duplicate checking)

4.  **Persistence**:
    - Appends data immediately to `data/raw/sauto_raw_data.csv`.
    - Uses a `seen_urls` set to ensure **0% duplicates**.

## 🚀 How to Run

Navigate to the project root and execute the module:

```bash
python src/scraper/sauto_scraper.py
```

*Note: The first time you run it, you may need to manually click the Cookie banner if the automated clicker misses it, then press ENTER in the terminal.*
