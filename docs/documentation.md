# Real Estate Market Analyzer - Project Documentation

## 1. Project Overview
The **Real Estate Market Analyzer** is a desktop application designed to estimate the market price of apartments in the Czech Republic. It uses machine learning models trained on current market data to provide users with value estimates and 10-year growth projections.

### Design Goals
- **Domain Pivot**: Adapted from the original car market logic to handle real estate specificities (dispositions, size, regional pricing).
- **Clarity**: Simple Czech-localized interface for easy property evaluation.

---

## 2. Implementation Details

### A. Data Collection (`src/scraper/`)
- **Target**: `reality.idnes.cz` (Byty / Prodej).
- **Features**: Disposition, Area, Locality, Price.

### B. Machine Learning (`src/model/`)
- **Model**: Random Forest Regressor.
- **Features**: `area` (m2), `disposition` (1+kk, 2+1 etc.), `region`.

### C. GUI Application (`src/app/`)
- Built with Tkinter and Matplotlib for data visualization.
- Uses a dark-mode theme optimized for professional analysis.

---

## 3. Maintenance

To update the system with new market data:
1. Run `python src/scraper/reality_scraper.py`.
2. Run `python src/model/train_model.py` to retrain the model on the fresh dataset.
