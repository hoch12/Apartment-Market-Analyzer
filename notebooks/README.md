# Car Price Prediction Analysis

This directory contains the Jupyter Notebooks used for Exploratory Data Analysis (EDA) and Model Training.

## 📊 Process Overview

### 1. Data Loading & Cleaning
- **Source**: Loaded raw data from `data/raw/sauto_raw_data.csv`.
- **Cleaning**:
    - Parsed `2018` from strings like `Rok výroby: 2018`.
    - Converted mileage (`120 000 km`) to integers (`120000`).
    - Standardized fuel types (consolidated similar names).
- **Filtering**: Removed outliers (e.g., cars with 0 price or > 1,000,000 km mileage).

### 2. Feature Engineering
- **One-Hot Encoding**: Transformed categorical variables (`Brand`, `Fuel`, `Transmission`) into binary vectors suitable for machine learning algorithms.
- **Correlation Matrix**: Analyzed the relationship between features. Key insight: Mileage has a strong negative correlation with Price (approx -0.6).

### 3. Model Training
- **Algorithm**: **Random Forest Regressor** (Ensemble of 100 Decision Trees).
- **Split**: 80% Training / 20% Testing.
- **Validation**: Achieved an R² score of ~0.85 on test data, indicating high predictive accuracy.

### 4. Evaluation & Charts
The notebook generates several visualizations to validate the model:
- **Actual vs. Predicted Price**: A scatter plot showing how close predictions are to real values (ideal is a diagonal line).
- **Feature Importance**: A bar chart highlighting that **Year of Manufacture** and **Mileage** are the most critical factors driving price.

## 🚀 Usage

To reproduce the analysis or retrain the model:

```bash
jupyter notebook notebooks/Car_Price_Prediction.ipynb
```
