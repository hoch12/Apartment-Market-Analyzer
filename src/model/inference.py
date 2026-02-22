import os
import joblib
import pandas as pd
import datetime
import json
from src.utils.config_loader import ConfigLoader

class PricePredictor:
    """
    Handles model loading and price prediction inference.
    
    Attributes:
        model (RandomForestRegressor): The trained sklearn model.
        model_columns (list): List of feature names expected by the model.
        metadata (dict): Additional metadata (regions, valid ranges) loaded from JSON.
    """
    def __init__(self, model_path=None, columns_path=None):
        """
        Initialize the predictor and load model artifacts.

        Args:
            model_path (str, optional): Custom path to .pkl model file.
            columns_path (str, optional): Custom path to .pkl columns file.
        """
        self.model = None
        self.model_columns = None
        self.current_year = datetime.datetime.now().year
        self.config = ConfigLoader.get_config()
        self.model_config = self.config.get('model', {})
        self.paths_config = self.config.get('paths', {})
        self.metadata = None
        
        # Resolve absolute paths relative to project root
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        model_filename = self.paths_config.get('model_filename', 'apartment_price_model.pkl')
        columns_filename = self.paths_config.get('columns_filename', 'apartment_columns.pkl')
        
        model_folder = self.paths_config.get('model_folder', os.path.join('src', 'model'))
        base_model_path = os.path.join(root, model_folder)
        
        final_model_path = model_path or os.path.join(base_model_path, model_filename)
        final_columns_path = columns_path or os.path.join(base_model_path, columns_filename)
        
        try:
            self.load_model_data(final_model_path, final_columns_path)
        except Exception as e:
            print(f"Warning: Could not load model: {e}")

    def load_model_data(self, model_path, columns_path):
        """Load model and column definitions from disk."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        if not os.path.exists(columns_path):
            raise FileNotFoundError(f"Model columns not found: {columns_path}")

        self.model = joblib.load(model_path)
        self.model_columns = joblib.load(columns_path)
        
        # Load Metadata
        metadata_path = os.path.join(os.path.dirname(model_path), 'apartment_metadata.json')
        if os.path.exists(metadata_path):
             with open(metadata_path, 'r', encoding='utf-8') as f:
                  self.metadata = json.load(f)
        else:
             self.metadata = None

    def get_regions(self):
        """Return list of valid regions."""
        if self.metadata:
            return self.metadata.get('regions', [])
        return self.model_config.get('regions', [])

    def get_dispositions(self):
        """Return list of valid dispositions."""
        if self.metadata:
            return self.metadata.get('dispositions', [])
        return list(self.model_config.get('disposition_mapping', {}).keys())

    def predict_price(self, area, disposition, region):
        """
        Predict the price of an apartment.

        Args:
            area (float): Area in m^2.
            disposition (str): Disposition category (e.g. '2+kk').
            region (str): Region name (e.g. 'Praha').

        Returns:
            float: Predicted price.
        """
        if self.model is None or self.model_columns is None:
            raise ValueError("Model not loaded")

        # 1. Create input dictionary with zeros
        input_data = {col: 0 for col in self.model_columns}

        # 2. Set numerical values
        input_data['area'] = area

        # 3. Set categorical values (One-Hot Encoding)
        disp_col = f"disposition_{disposition}"
        region_col = f"region_{region}"

        if disp_col in input_data:
            input_data[disp_col] = 1
        
        if region_col in input_data:
            input_data[region_col] = 1

        # 4. Create DataFrame and ensure column order
        encoded_df = pd.DataFrame([input_data])
        encoded_df = encoded_df[self.model_columns]

        # 5. Predict
        price = self.model.predict(encoded_df)[0]
        return price

    def calculate_future_value(self, start_price, years=10, growth_rate=0.03):
        """
        Calculate future value projections based on compound annual growth rate.
        
        Args:
            start_price (float): Initial price.
            years (int): Number of years to project.
            growth_rate (float): Annual growth rate (e.g. 0.03 for 3%).

        Returns:
            list[dict]: List of dicts with 'year' and 'price'.
        """
        future_values = []
        current_val = start_price
        start_year_val = self.current_year
        
        # Current year
        future_values.append({'year': start_year_val, 'price': current_val})

        # Next 'years' years
        for i in range(1, years + 1):
            current_val = current_val * (1 + growth_rate)
            future_values.append({'year': start_year_val + i, 'price': current_val})
            
        return future_values
