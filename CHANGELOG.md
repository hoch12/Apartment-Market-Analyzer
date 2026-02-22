# Changelog

All notable changes to the "Apartment Market Analyzer" project will be documented in this file.

## [1.0.1] - 2026-02-22
### Changed
- **Documentation**: Added instructions for virtual environment (`.venv`) setup and activation to `README.md` and `docs/documentation.md`.
- **Configuration**: Extracted all hardcoded configuration parameters (limits, model paths, training constants, cities) from Python modules (`gui_app.py`, `train_model.py`, `inference.py`) into the central `config.json` file.
- **Config Documentation**: Added detailed english pseudo-comments directly inside `config.json` explaining what each field does and how safely users can tweak the app behavior. Removed unused `foreign_countries` configuration logic limit.

## [1.0.0] - 2026-02-19
### **Gold Master Release**
- **Full Release**: The project is now stable and fully pivoted to real estate analysis.
- **Data**: Trained on a verified dataset of **5300+ apartments**.
- **Documentation**: Translated all documentation to English and added comprehensive run instructions.
- **Code Quality**: Added docstrings to all source modules for better maintainability.


## [0.9.0] - Pre-release
### Added
- **Smart Validation**: The GUI now warns users when inputting unrealistic parameters (e.g., 65m² for a 6+kk apartment).
- **Large Scale Training**: Successfully retrained the Random Forest model on a massive dataset (5000+ items).
- **Error Handling**: Scraper now gracefully handles start page limits and browser disconnects.

## [0.8.0] - Model Refinement
### Fixed
- **Region Logic**: Fixed a critical bug where cities (Brno, Ostrava) were not correctly mapped to their regions, causing poor predictions.
- **GUI Styling**: Replaced incompatible `tk.Button` with `ttk.Button` for correct rendering on macOS dark mode.
- **Metadata**: Generated a comprehensive list of valid regions for the UI dropdown.

## [0.7.0] - Scraper Optimization
### Changed
- **Config**: Increased scraping limit to 500 pages to capture more market data.
- **Stability**: Added manual intervention step for stubborn cookie consent popups.
- **Resilience**: Scraper state is now saved per page to allow resuming after interruptions.

## [0.6.0] - The Great Pivot
### Changed
- **Total Refactor**: Renamed project focus from "Car Market Analyzer" to "Apartment Market Analyzer".
- **Core Logic**:
    - Replaced `sauto_scraper` with `reality_scraper` (targeting reality.idnes.cz).
    - Updated `PricePredictor` to use `area` (m²), `disposition` (e.g., 2+kk), and `region`.
- **UI**: Redesigned the interface to match real estate terminology.
- **Notebooks**: Created `Apartment_Price_Analysis.ipynb` for EDA.

---

## [Legacy Versions]
*All versions prior to 0.6.0 pertained to the "Car Market Analyzer" and are now obsolete.*