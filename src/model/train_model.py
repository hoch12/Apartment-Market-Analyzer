import pandas as pd
import numpy as np
import re
import os
import joblib
import json
from sklearn.ensemble import RandomForestRegressor
import sys

# Increase recursion depth if needed
sys.setrecursionlimit(2000)

# --- CONFIG ---
RAW_DATA_PATH = 'data/raw/apartments_raw_data.csv'
MODEL_PATH = 'src/model/apartment_price_model.pkl'
COLUMNS_PATH = 'src/model/apartment_columns.pkl'
METADATA_PATH = 'src/model/apartment_metadata.json'

def parse_area(title):
    # Matches "54 m²" or "54m2"
    match = re.search(r'(\d+)\s*m[²2]', str(title))
    if match:
        return int(match.group(1))
    return None

def parse_disposition(title):
    # Matches "2+kk", "1+1", "3+1" etc.
    match = re.search(r'(\d\+[\w]{1,2})', str(title))
    if match:
        return match.group(1)
    return 'Other'

def clean_region(location):
    location = str(location)
    
    # Map of major cities/districts to regions
    city_to_region = {
        'Praha': 'Praha',
        'Brno': 'Jihomoravský kraj',
        'Ostrava': 'Moravskoslezský kraj',
        'Plzeň': 'Plzeňský kraj',
        'Liberec': 'Liberecký kraj',
        'Olomouc': 'Olomoucký kraj',
        'České Budějovice': 'Jihočeský kraj',
        'Hradec Králové': 'Královéhradecký kraj',
        'Ústí nad Labem': 'Ústecký kraj',
        'Pardubice': 'Pardubický kraj',
        'Karlovy Vary': 'Karlovarský kraj',
        'Jihlava': 'Kraj Vysočina',
        'Zlín': 'Zlínský kraj',
        'Středočeský': 'Středočeský kraj',
        'Kladno': 'Středočeský kraj',
        'Mladá Boleslav': 'Středočeský kraj',
        'Příbram': 'Středočeský kraj',
        'Kolín': 'Středočeský kraj',
        'Benešov': 'Středočeský kraj',
        'Beroun': 'Středočeský kraj',
        'Mělník': 'Středočeský kraj',
        'Most': 'Ústecký kraj',
        'Děčín': 'Ústecký kraj',
        'Teplice': 'Ústecký kraj',
        'Chomutov': 'Ústecký kraj',
        'Frýdek-Místek': 'Moravskoslezský kraj',
        'Karviná': 'Moravskoslezský kraj',
        'Opava': 'Moravskoslezský kraj',
        'Havířov': 'Moravskoslezský kraj',
        'Třinec': 'Moravskoslezský kraj',
        'Znojmo': 'Jihomoravský kraj',
        'Břeclav': 'Jihomoravský kraj',
        'Hodonín': 'Jihomoravský kraj',
        'Vyškov': 'Jihomoravský kraj',
        'Blansko': 'Jihomoravský kraj',
        'Prostějov': 'Olomoucký kraj',
        'Přerov': 'Olomoucký kraj',
        'Šumperk': 'Olomoucký kraj',
        'Vsetín': 'Zlínský kraj',
        'Uherské Hradiště': 'Zlínský kraj',
        'Kroměříž': 'Zlínský kraj',
        'Tábor': 'Jihočeský kraj',
        'Písek': 'Jihočeský kraj',
        'Strakonice': 'Jihočeský kraj',
        'Jindřichův Hradec': 'Jihočeský kraj',
        'Český Krumlov': 'Jihočeský kraj',
        'Cheb': 'Karlovarský kraj',
        'Sokolov': 'Karlovarský kraj',
        'Třebíč': 'Kraj Vysočina',
        'Havlíčkův Brod': 'Kraj Vysočina',
        'Žďár nad Sázavou': 'Kraj Vysočina',
        'Pelhřimov': 'Kraj Vysočina',
        'Chrudim': 'Pardubický kraj',
        'Svitavy': 'Pardubický kraj',
        'Ústí nad Orlicí': 'Pardubický kraj',
        'Jablonec nad Nisou': 'Liberecký kraj',
        'Česká Lípa': 'Liberecký kraj',
        'Semily': 'Liberecký kraj',
        'Trutnov': 'Královéhradecký kraj',
        'Náchod': 'Královéhradecký kraj',
        'Jičín': 'Královéhradecký kraj',
        'Rychnov nad Kněžnou': 'Královéhradecký kraj',
        'Tachov': 'Plzeňský kraj',
        'Klatovy': 'Plzeňský kraj',
        'Domažlice': 'Plzeňský kraj',
        'Rokycany': 'Plzeňský kraj'
    }

    # First check explicit foreign countries to avoid misclassification
    foreign_countries = ['Španělsko', 'Egypt', 'Albánie', 'Bulharsko', 'Chorvatsko', 'Slovensko', 'Rakousko', 'Německo', 'Kapverdy', 'Spojené arabské emiráty', 'Thajsko', 'Indonézie', 'Kypr', 'Černá Hora']
    for country in foreign_countries:
        if country in location:
            return 'Zahraničí'

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
    df = df[df['price'] > 100000] # Realistic floor for apartments

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
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("Model training complete.")

    # 6. Save Artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(list(X.columns), COLUMNS_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Columns saved to {COLUMNS_PATH}")

if __name__ == "__main__":
    train()
