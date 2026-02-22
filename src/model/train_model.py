import pandas as pd
import numpy as np
import re
import os
import joblib
import json
from sklearn.ensemble import RandomForestRegressor
import sys

# Init path to access shared utils
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.utils.config_loader import ConfigLoader
config = ConfigLoader.get_config()

# Increase recursion depth if needed
sys.setrecursionlimit(2000)

# --- CONFIG ---
RAW_DATA_PATH = os.path.join(project_root, config['paths']['output_folder'], config['paths']['output_filename'])
MODEL_PATH = os.path.join(project_root, config['paths']['model_folder'], config['paths']['model_filename'])
COLUMNS_PATH = os.path.join(project_root, config['paths']['model_folder'], config['paths']['columns_filename'])
METADATA_PATH = os.path.join(project_root, config['paths']['model_folder'], config['paths']['metadata_filename'])

def parse_area(title):
    """
    Extract area in square meters from the title string.

    Args:
        title (str): Title containing area (e.g. "Prodej bytu 3+kk 75 m²").

    Returns:
        int or None: Extracted area or None if not found.
    """
    # Matches "54 m²" or "54m2"
    match = re.search(r'(\d+)\s*m[²2]', str(title))
    if match:
        return int(match.group(1))
    return None

def parse_disposition(title):
    """
    Extract apartment disposition (e.g. 2+kk) from the title.

    Args:
        title (str): Title string.

    Returns:
        str: Disposition string or 'Other'.
    """
    # Matches "2+kk", "1+1", "3+1" etc.
    match = re.search(r'(\d\+[\w]{1,2})', str(title))
    if match:
        return match.group(1)
    return 'Other'

def clean_region(location):
    """
    Map a specific location string (city/district) to a general Region (Kraj).

    Args:
        location (str): Raw location string.

    Returns:
        str: Normalized region name or 'Other'/'Zahraničí'.
    """
    location = str(location)
    
    city_to_region = config['model']['city_to_region']

    # Check for cities in the location string
    for city, region in city_to_region.items():
        if city in location:
            return region

    # Fallback checks for keywords
    if 'Praha' in location: return 'Praha'
    if 'Středočeský' in location: return 'Středočeský kraj'
    if 'Jihočeský' in location: return 'Jihočeský kraj'
    if 'Plzeňský' in location: return 'Plzeňský kraj'
    if 'Karlovarský' in location: return 'Karlovarský kraj'
    if 'Ústecký' in location: return 'Ústecký kraj'
    if 'Liberecký' in location: return 'Liberecký kraj'
    if 'Královéhradecký' in location: return 'Královéhradecký kraj'
    if 'Pardubický' in location: return 'Pardubický kraj'
    if 'Vysočina' in location: return 'Kraj Vysočina'
    if 'Jihomoravský' in location: return 'Jihomoravský kraj'
    if 'Olomoucký' in location: return 'Olomoucký kraj'
    if 'Zlínský' in location: return 'Zlínský kraj'
    if 'Moravskoslezský' in location: return 'Moravskoslezský kraj'

    return 'Other'

def train():
    """
    Main training pipeline:
    1. Loads raw CSV data.
    2. Extracts features (area, disposition, region).
    3. Cleans data (removes outliers, parses prices).
    4. Generates metadata for UI.
    5. Trains RandomForestRegressor.
    6. Saves model and artifacts.
    """
    print("Loading apartment data...")
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: {RAW_DATA_PATH} not found. Run scraper first.")
        return

    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded {len(df)} rows.")

    # 1. Feature Extraction
    print("Extracting features...")
    df['area'] = df['title'].apply(parse_area)
    df['disposition'] = df['title'].apply(parse_disposition)
    df['region'] = df['location'].apply(clean_region)

    # 2. Cleaning
    print("Cleaning data...")
    df['price'] = df['raw_price'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    print("\n--- Missing Values Check ---")
    print(df[['area', 'disposition', 'price', 'region']].isnull().sum())
    
    df = df.dropna(subset=['area', 'price'])
    min_price = config['model']['training']['min_price']
    df = df[df['price'] > min_price] # Realistic floor for apartments

    # 3. Generate Metadata (Valid Options for UI)
    print("Generating metadata...")
    metadata = {
        'dispositions': sorted(df['disposition'].unique().tolist()),
        'regions': sorted(df['region'].unique().tolist()),
        'min_area': int(df['area'].min()),
        'max_area': int(df['area'].max())
    }

    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Metadata saved to {METADATA_PATH}")

    # 4. Prepare for Training
    features = ['area', 'disposition', 'region']
    X = df[features]
    y = df['price']

    # One-Hot Encoding
    X = pd.get_dummies(X, columns=['disposition', 'region'], drop_first=False)
    
    # 5. Train Model
    print("\nTraining Random Forest Regressor...")
    n_est = config['model']['training']['rf_n_estimators']
    r_state = config['model']['training']['rf_random_state']
    model = RandomForestRegressor(n_estimators=n_est, random_state=r_state)
    model.fit(X, y)
    print("Model training complete.")

    # 6. Save Artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(list(X.columns), COLUMNS_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Columns saved to {COLUMNS_PATH}")

if __name__ == "__main__":
    train()
