# Changelog

## [0.6.0] - 2026-02-19
### Changed
- **Total Project Pivot:**
    - Converted "Car Market Analyzer" to **"Apartment Market Analyzer"**.
    - Replaced car-related logic with real estate analysis (Apartments/Byty).
- **Architecture Refactoring:**
    - Created `reality_scraper.py` targeting real estate portals instead of car marketplaces.
    - Refactored `train_model.py` and `inference.py` to handle features like Area (m2), Disposition, and Region.
    - Completely redesigned `gui_app.py` with a new "Real Estate" theme and relevant property inputs.
- **Documentation:**
    - Updated `README.md` and internal documentation to reflect the new real estate focus.
    - Updated `config.json` with property-specific metadata and aesthetics.

## [0.5.0] - 2026-02-19
### Added
- **Data Acquisition Procedure:**
    - Created a new workflow `/download-data` for expanding the dataset.
    - Updated `src/scraper/README.md` with instructions on how to download more data.
    - Added a "Data Maintenance & Expansion" section to the main documentation.
    - Implemented a resume logic reminder in the configuration guide.

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
- **Robust Error Handling & Validation:**
    - Validates user input against reliable `model_metadata.json`.
    - Displays specific error messages (e.g., "Škoda with Diesel not found") instead of crashing.
    - **Year Range Guard:** Added warnings for years outside the specific brand's training data range.
    - **Mileage Sanity Check:** Implemented warnings for unrealistically low mileage in older vehicles to prevent over-inflated predictions.

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
- **Web Scraper:**
    - Built `src/scraper/sauto_scraper.py` using Selenium.
    - Implemented infinite scrolling and pagination logic.
    - Added extraction of key features (Year, Mileage, Power, Fuel).
- **Data Collection:**
    - Collected initial dataset of >2000 listings from Sauto.cz.

## [0.1.0] - 2026-02-08
### Added
- **Project Structure:**
    - Initialized Git repository and virtual environment.
    - Set up directory layout (`src/`, `data/`, `tests/`).