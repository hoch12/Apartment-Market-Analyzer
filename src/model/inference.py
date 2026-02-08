import os
import joblib
import pandas as pd
import datetime

class PricePredictor:
    def __init__(self, model_path=None, columns_path=None):
        self.model = None
        self.model_columns = None
        self.current_year = datetime.datetime.now().year
        
        if model_path and columns_path:
            self.load_model_data(model_path, columns_path)
        else:
            # Default paths relative to this file
            base_path = os.path.dirname(os.path.abspath(__file__))
            default_model_path = os.path.join(base_path, 'car_price_model.pkl')
            default_columns_path = os.path.join(base_path, 'model_columns.pkl')
            self.load_model_data(default_model_path, default_columns_path)

    def load_model_data(self, model_path, columns_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        if not os.path.exists(columns_path):
            raise FileNotFoundError(f"Model columns not found: {columns_path}")

        self.model = joblib.load(model_path)
        self.model_columns = joblib.load(columns_path)

    def get_clean_brands(self):
        if self.model_columns is None:
            return []

        clean_brands = []
        for col in self.model_columns:
            if col.startswith('brand_'):
                brand_name = col.replace('brand_', '')
                # Filter out garbage
                if "http" in brand_name or "www" in brand_name or ".cz" in brand_name:
                    continue
                if len(brand_name) > 20:
                    continue
                clean_brands.append(brand_name)

        return sorted(clean_brands)

    def predict_price(self, year, mileage, brand, fuel, transmission):
        if self.model is None or self.model_columns is None:
            raise ValueError("Model not loaded")

        # 1. Create input dictionary with zeros
        input_data = {col: 0 for col in self.model_columns}

        # 2. Set numerical values
        input_data['year'] = year
        input_data['mileage'] = mileage

        # 3. Set categorical values (One-Hot Encoding with Mapping)
        brand_col = f"brand_{brand}"
        if brand_col in input_data:
            input_data[brand_col] = 1

        # Fuel Mapping
        # GUI: ['Petrol', 'Diesel', 'Electric', 'LPG', 'Hybrid', 'CNG']
        # Model: ['fuel_Elektro', 'fuel_Hybridní', 'fuel_Nafta', 'fuel_Other']
        # Missing: Petrol (Reference), LPG, CNG
        fuel_map = {
            'Petrol': None,       # Reference category (all 0s)
            'Diesel': 'fuel_Nafta',
            'Electric': 'fuel_Elektro',
            'Hybrid': 'fuel_Hybridní',
            'LPG': 'fuel_Other',  # Map to Other
            'CNG': 'fuel_Other'   # Map to Other
        }
        
        target_fuel = fuel_map.get(fuel, 'fuel_Other') # Default to Other if unknown
        if target_fuel and target_fuel in input_data:
            input_data[target_fuel] = 1

        # Transmission Mapping
        # GUI: ['Manual', 'Automatic']
        # Model: ['transmission_Manual', 'transmission_Manuální']
        # Note: Model might have duplicate columns or 'Manual' is the one to use.
        # Based on previous inspection, 'transmission_Manuální' exists.
        trans_map = {
            'Manual': 'transmission_Manuální',
            'Automatic': None   # Reference category
        }
        
        target_trans = trans_map.get(transmission, None)
        if target_trans and target_trans in input_data:
            input_data[target_trans] = 1
        elif target_trans is None and transmission == 'Manual':
             # Fallback if 'transmission_Manuální' not found but 'transmission_Manual' exists
             if 'transmission_Manual' in input_data:
                 input_data['transmission_Manual'] = 1

        # 4. Create DataFrame and ensure column order
        encoded_df = pd.DataFrame([input_data])
        encoded_df = encoded_df[self.model_columns]

        # 5. Predict
        price = self.model.predict(encoded_df)[0]
        return price

    def calculate_future_value(self, start_price, years=5, depreciation_rate=0.10):
        future_values = []
        current_val = start_price
        start_year_val = self.current_year
        
        # Current year
        future_values.append({'year': start_year_val, 'price': current_val})

        # Next 'years' years
        for i in range(1, years + 1):
            current_val = current_val * (1 - depreciation_rate)
            future_values.append({'year': start_year_val + i, 'price': current_val})
            
        return future_values
