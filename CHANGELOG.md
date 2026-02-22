# Changelog

All notable changes to the "Apartment Market Analyzer" project will be documented in this file.

## [1.0.3] - 2026-02-22
### Changed
- **Documentation**: Added instructions for virtual environment (`.venv`) setup and activation to `README.md` and `docs/documentation.md`.
- **Configuration**: Extracted all hardcoded configuration parameters (limits, model paths, training constants, cities) from Python modules (`gui_app.py`, `train_model.py`, `inference.py`) into the central `config.json` file.
- **Config Documentation**: Added detailed english pseudo-comments directly inside `config.json` explaining what each field does and how safely users can tweak the app behavior. Removed unused `foreign_countries` configuration logic limit.

## [1.0.2] - 2026-02-22
### Changed
- **Data & Model**: The application was freshly retrained on a massively expanded dataset scraped from reality.idnes.cz. The Random Forest Regressor now utilizes the power of over **10,000+ apartment ads** (up from 5,300), significantly increasing its predictive robustness across all 14 Czech regions.

## [1.0.1] - 2026-02-22
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

## [Legacy Versions - Car Market Analyzer]
*All versions prior to 0.6.0 pertained to the "Car Market Analyzer" and are preserved here for historical context.*

## [0.5.1] - 2026-02-18
### Added
- **GUI Improvements**: Added user-friendly formatting for large numbers (e.g., 5.0M, 600k).
- **Price Range Restrictions**: Model throws Error if price is under 10 000 CZK (junk data protection).

## [0.5.0] - 2026-02-18
### Added
- **Car Depreciation Graph**: Added dynamic matplotlib chart plotting expected car value decrease over 10 years based on a 7% annual depreciation rate.

### Changed
- **Model Refinement**:
    - **Year Range Guard:** Added warnings for years outside the specific brand's training data range.
    - **Mileage Sanity Check:** Implemented warnings for unrealistically low mileage in older vehicles to prevent over-inflated predictions.

## [0.4.0] - 2026-02-08
### Changed
- **Localization:**
    - Switched entire application (GUI, Config, Model) to **Czech language** for consistency with dataset.
    - Updated `config.json` mappings to use Czech keys (`Benzín`, `Nafta`...).
- **Model Accuracy:**
    - **Retrained Model:** Fixed "Identical Price" issue utilizing new data cleaning pipeline.
    - **Brand Normalization:** Implemented advanced parsing to extract brands from URLs and normalize mixed case (e.g. "bmw" -> "BMW").
    - **Data Recovery:** Recovered ~2000 listings that were previously discarded due to malformed titles.

### Added
- **Robust Error Handling:**
    - Validates user input against reliable `model_metadata.json`.
    - Displays specific error messages (e.g., "Škoda with Diesel not found") instead of crashing.

## [0.3.0] - 2026-02-08
### Added
- **Localization System:**
    - Implemented full English localization for the GUI (Labels, Buttons, Dropdowns).
    - Updated `PricePredictor` to map English inputs ('Petrol', 'Diesel') to internal model columns.
    - Localized all internal code comments and docstrings.

### Changed
- **UI Experience:**
    - Enhanced contrast by changing "CALCULATE" button text to **black**.
    - Optimized window geometry (`800x950`) for MacOS.
    - Standardized typography using `Segoe UI`.

## [0.2.4] - 2026-02-08
### Added
- **Documentation:**
    - Created `docs/documentation.md` covering Design, Analysis, and Implementation.
    - Rewrote `README.md` with comprehensive setup instructions and visual architecture.

## [0.2.3] - 2026-02-08
### Added
- **Architecture Refactoring:**
    - Extracted prediction logic into `src/model/inference.py`.
    - Created `PricePredictor` class for better modularity and testing.
    - Added unit tests in `tests/test_inference.py`.

### Fixed
- **Performance:**
    - Fixed Matplotlib memory leak by moving to the object-oriented `Figure` API.

## [0.2.2] - 2026-02-08
### Fixed
- **Critical Bugs:**
    - Fixed "Identical Price" bug by implementing valid fuel mapping for LPG/CNG.
    - Corrected "off-by-one" error in future value projection (2026-2030).
    - Fixed scientific notation in graph labels (now uses 'k', 'M').

## [0.2.1] - 2026-02-08
### Added
- **Machine Learning Integration:**
    - Developed `notebooks/Car_Price_Prediction.ipynb` for EDA and training.
    - Implemented data cleaning pipeline (parsing years, mileage).
    - Trained Random Forest Regressor and exported artifacts (`car_price_model.pkl`).

## [0.2.0] - 2026-02-08
### Added
- **Web Scraper Module:**
    - Developed `src/scraper/sauto_scraper.py` using Selenium.
    - Implemented robust logic for pagination, cookie handling, and lazy-loading scrolling.
    - Added `config.json` for external configuration management.
    - Implemented state saving (`scraper_state.json`) to allow pausing and resuming downloads.
- **Data Collection:**
    - Successfully scraped over 2000 unique vehicle records from Sauto.cz.
    - Created dataset structure: `data/raw/` and `data/processed/`.
- **Machine Learning Pipeline:**
    - Created Jupyter Notebook `notebooks/Car_Price_Prediction.ipynb` for data analysis.
    - Implemented data cleaning functions (parsing price, year, mileage from text descriptions).
    - Trained a Random Forest Regressor model with successful evaluation charts.
    - Exported trained artifacts: `car_price_model.pkl` and `model_columns.pkl`.

### Changed
- Updated `.gitignore` to exclude large raw data files and virtual environment artifacts.
- Refactored project structure to separate source code (`src`) from notebooks and data.

## [0.1.0] - 2026-02-08
### Added
- Initial project structure setup based on assignment requirements.
- Git repository initialization.
- Documentation folder for future analysis and design documents.