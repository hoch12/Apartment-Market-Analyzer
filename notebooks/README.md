# Apartment Price Prediction Analysis

This directory contains the Jupyter Notebooks used for Exploratory Data Analysis (EDA) and Model Training.

## 📊 Process Overview

### 1. Data Loading & Cleaning
- **Source**: Loaded raw data from `data/raw/apartments_raw_data.csv`.
- **Cleaning**:
    - Parsed price strings (removing non-numeric characters).
    - Standardized disposition types (consolidated similar layouts).
    - Mapped cities to regions.
- **Filtering**: Removed outliers (e.g., apartments with 0 price or unrealistic area).

### 2. Feature Engineering
- **One-Hot Encoding**: Transformed categorical variables (`Region`, `Disposition`) into binary vectors suitable for machine learning algorithms.
- **Correlation Matrix**: Analyzed the relationship between features. Key insight: Area has a strong positive correlation with Price.

### 3. Model Training
- **Algorithm**: **Random Forest Regressor** (Ensemble of Decision Trees).
- **Split**: 80% Training / 20% Testing.
- **Validation**: Achieved high accuracy on test data.

### 4. Evaluation & Charts
The notebook generates several visualizations to validate the model:
- **Actual vs. Predicted Price**: A scatter plot showing how close predictions are to real values.
- **Feature Importance**: A chart highlighting that **Area** and **Region** are critical factors driving price.

## 🚀 Usage

To reproduce the analysis or retrain the model interactively:

```bash
jupyter notebook notebooks/Apartment_Price_Analysis.ipynb
```
