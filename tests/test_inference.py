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
        self.predictor.model.predict.return_value = [5000000]
        self.predictor.model_columns = [
            'area', 
            'disposition_2+kk', 'disposition_3+1', 
            'region_Praha', 'region_Brno'
        ]

    def test_predict_price(self):
        # PricePredictor.predict_price(area, disposition, region)
        price = self.predictor.predict_price(
            area=60, 
            disposition='2+kk', 
            region='Praha'
        )
        self.assertEqual(price, 5000000)
        
        # Check if predict was called with correct dataframe shape
        args, _ = self.predictor.model.predict.call_args
        df = args[0]
        self.assertEqual(df.shape, (1, 5))
        self.assertEqual(df.iloc[0]['disposition_2+kk'], 1)
        self.assertEqual(df.iloc[0]['region_Praha'], 1)
        self.assertEqual(df.iloc[0]['area'], 60)

    def test_calculate_future_value(self):
        start_price = 1000000
        # calculate_future_value(start_price, years, growth_rate)
        future_values = self.predictor.calculate_future_value(start_price, years=2, growth_rate=0.05)
        
        current_year = datetime.datetime.now().year
        
        self.assertEqual(len(future_values), 3) # start + 2 years
        self.assertEqual(future_values[0]['year'], current_year)
        self.assertEqual(future_values[0]['price'], 1000000)
        
        self.assertEqual(future_values[1]['year'], current_year + 1)
        self.assertEqual(future_values[1]['price'], 1050000) # 1M + 5%

        self.assertEqual(future_values[2]['year'], current_year + 2)
        self.assertAlmostEqual(future_values[2]['price'], 1102500) # 1.05M + 5%

if __name__ == '__main__':
    unittest.main()
