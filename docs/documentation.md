# Apartment Market Analyzer - User Manual v1.0

**Apartment Market Analyzer** is a desktop application for analyzing the real estate market in the Czech Republic. It serves to estimate the market price of apartments and predict the future development of their value using machine learning.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or newer
- Google Chrome (for data downloading)

### Installation & Setup
1. Clone the repository (or download ZIP).
2. Create and activate a virtual environment:
   **Mac/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   **Windows:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To start the graphical interface:
```bash
python src/app/gui_app.py
```

## 🛠 Features and Usage

### 1. Price Estimation
In the main application window, fill in:
- **Region**: Location where the apartment is situated.
- **Disposition**: Type of apartment (e.g., 2+kk, 3+1).
- **Area**: Usable area in square meters.

Click on **ANALYZE MARKET PRICE**. The application will display:
- Estimated current market price.
- Graph of value development prediction for 10 years ahead.

> **Smart Validation**: The application will warn you if you enter a nonsensical combination (e.g., 6+kk with a size of 20 m²).

### 2. Data Downloading (Scraping)
If you want to update the database of ads from reality.idnes.cz:
```bash
python src/scraper/reality_scraper.py
```
- The script opens a browser.
- **IMPORTANT**: You must manually confirm cookies in the browser and press ENTER in the terminal.
- Data is saved to `data/raw/apartments_raw_data.csv`.

### 3. Model Training
After downloading new data, you can retrain the model for higher accuracy:
```bash
python src/model/train_model.py
```
- The model is saved to `src/model/apartment_price_model.pkl`.

### 4. Analysis in Notebook
For detailed data exploration (graphs, statistics), use Jupyter Notebook:
- Open the file `notebooks/Apartment_Price_Analysis.ipynb` in VS Code or Jupyter Lab.

### 5. Configuration (`config.json`)
The entire application behavior (GUI thresholds, model paths, dataset regions, Selenium webdriver rules) is centralized in `config.json`.
- Inside the file, you will find extensive **English pseudo-comments** (keys starting with `"_comment"`).
- These comments serve as a built-in manual telling you what is safe to edit and what it affects.
- Feel free to modify the values (e.g. increase `num_pages` for the scraper, or change `bg_primary` hex color for the GUI) to fit your needs.

## 🧠 How it works?

### Data
The application uses a robust dataset containing over **10,000 real estate ads**, which contain information about:
- Price
- Disposition (1+kk to 6+kk)
- Area (m²)
- Location (region/city)

### Machine Learning Model
We use the **Random Forest Regressor** algorithm, which learns relationships between these parameters.
- **Validation**: Data outside logical bounds (e.g., extremely cheap apartments) are ignored during training.
- **Location**: Cities are automatically mapped to respective regions for better generalization.

## ⚠️ Known Limitations
- Predictions for very specific locations (small villages) might be less accurate than for large cities.
- Future development estimation is a mathematical projection with fixed growth (4% annually) and does not account for macroeconomic shocks.

---
*Version 1.0.0 | © 2026 Apartment Market Analyzer Team*
