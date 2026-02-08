import unittest
import os
import sys
import datetime
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model.inference import PricePredictor

class TestPricePredictor(unittest.TestCase):
    def setUp(self):
        # Create a dummy predictor with mocked model
        self.predictor = PricePredictor(model_path=None, columns_path=None)
        # Manually inject mock model and columns
        self.predictor.model = MagicMock()
        self.predictor.model.predict.return_value = [200000]
        self.predictor.model_columns = [
            'year', 'mileage', 
            'brand_Skoda', 'brand_BMW', 
            'fuel_Benzín', 'fuel_Nafta', 
            'transmission_Manuální', 'transmission_Automatická'
        ]

    def test_get_clean_brands(self):
        self.predictor.model_columns = ['brand_Skoda', 'brand_BMW', 'brand_http://garbage.com', 'brand_VeryLongBrandNameThatShouldBeIgnored', 'year']
        brands = self.predictor.get_clean_brands()
        self.assertEqual(brands, ['BMW', 'Skoda'])

    def test_predict_price(self):
        price = self.predictor.predict_price(
            year=2020, 
            mileage=50000, 
            brand='Skoda', 
            fuel='Petrol', 
            transmission='Manual'
        )
        self.assertEqual(price, 200000)
        
        # Check if predict was called with correct dataframe shape
        args, _ = self.predictor.model.predict.call_args
        df = args[0]
        self.assertEqual(df.shape, (1, 8))
        self.assertEqual(df.iloc[0]['brand_Skoda'], 1)
        self.assertEqual(df.iloc[0]['brand_BMW'], 0)
        self.assertEqual(df.iloc[0]['year'], 2020)

    def test_calculate_future_value(self):
        start_price = 100000
        future_values = self.predictor.calculate_future_value(start_price, years=3, depreciation_rate=0.10)
        
        current_year = datetime.datetime.now().year
        
        self.assertEqual(len(future_values), 4) # start + 3 years
        self.assertEqual(future_values[0]['year'], current_year)
        self.assertEqual(future_values[0]['price'], 100000)
        
        self.assertEqual(future_values[1]['year'], current_year + 1)
        self.assertEqual(future_values[1]['price'], 90000) # 100k - 10%

        self.assertEqual(future_values[2]['year'], current_year + 2)
        self.assertEqual(future_values[2]['price'], 81000) # 90k - 10%

if __name__ == '__main__':
    unittest.main()
