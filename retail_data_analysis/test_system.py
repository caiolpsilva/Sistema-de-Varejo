import unittest
from zodb_model import ZODBHandler, Product
from mongodb_handler import MongoDBHandler
from sql_handler import MySQLHandler
from temporal_analysis import TemporalAnalysis
import pandas as pd

class TestRetailDataAnalysisSystem(unittest.TestCase):

    def setUp(self):
        # Setup handlers
        self.zodb_handler = ZODBHandler(db_path='test_retail_data.fs')
        self.mongo_handler = MongoDBHandler(db_name='test_retail_db')
        self.sql_handler = MySQLHandler(database='Varejobase')
        # Sample product
        self.product = Product(product_id=999, name="Test Product", category="Test Category", price=100.0, stock=10)
        self.zodb_handler.add_product(self.product)

    def tearDown(self):
        # Close connections and cleanup
        self.zodb_handler.close()
        self.mongo_handler.close()
        self.sql_handler.close()

    def test_zodb_add_and_get_product(self):
        product = self.zodb_handler.get_product(999)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product")

    def test_mongodb_insert_and_get_comment(self):
        comment_text = "Test comment"
        comment_id = self.mongo_handler.insert_comment(999, comment_text)
        self.assertIsNotNone(comment_id)
        comments = self.mongo_handler.get_comments(999)
        self.assertTrue(any(c['comment'] == comment_text for c in comments))

    def test_mysql_connection_and_query(self):
        query = "SELECT 1"
        result = self.sql_handler.execute_query(query)
        self.assertIsNotNone(result)

    def test_temporal_analysis_methods(self):
        # Create sample sales data
        data = {
            'date': pd.date_range(start='2023-01-01', periods=5),
            'product_id': [999]*5,
            'price': [100, 105, 110, 108, 107],
            'stock': [10, 9, 8, 7, 6],
            'sales': [1, 2, 3, 2, 1]
        }
        df = pd.DataFrame(data)
        ta = TemporalAnalysis(df)
        # Call methods to ensure no exceptions
        ta.historical_price_trend(999)
        ta.historical_stock_trend(999)
        future_dates, forecast = ta.forecast_sales(999, days=3)
        self.assertEqual(len(future_dates), 3)
        self.assertEqual(len(forecast), 3)

if __name__ == '__main__':
    unittest.main()
