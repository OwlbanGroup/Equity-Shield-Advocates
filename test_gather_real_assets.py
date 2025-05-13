import unittest
from unittest.mock import patch, mock_open
import gather_real_assets as gra

class TestGatherRealAssets(unittest.TestCase):

    @patch('gather_real_assets.yf.Ticker')
    def test_fetch_company_data_valid(self, mock_ticker):
        mock_ticker.return_value.info = {
            "shortName": "Test Company",
            "sector": "Technology",
            "marketCap": 1000000,
            "totalRevenue": 500000
        }
        result = gra.fetch_company_data("TEST")
        self.assertEqual(result['company'], "Test Company")
        self.assertEqual(result['ticker'], "TEST")
        self.assertEqual(result['sector'], "Technology")
        self.assertEqual(result['market_cap'], 1000000)
        self.assertEqual(result['revenue'], 500000)

    @patch('gather_real_assets.yf.Ticker')
    def test_fetch_company_data_exception(self, mock_ticker):
        mock_ticker.side_effect = Exception("API error")
        result = gra.fetch_company_data("FAIL")
        self.assertIsNone(result)

    @patch('gather_real_assets.fetch_company_data')
    def test_gather_data(self, mock_fetch):
        mock_fetch.side_effect = lambda ticker: {"ticker": ticker} if ticker != "FAIL" else None
        data = gra.gather_data()
        self.assertTrue(any(d['ticker'] == "GOOG" for d in data))
        self.assertTrue(any(d['ticker'] == "JPM" for d in data))
        self.assertTrue(any(d['ticker'] == "PLD" for d in data))

    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_json(self, mock_file):
        data = [{"company": "Test"}]
        gra.save_to_json(data, "test.json")
        mock_file.assert_called_with("test.json", "w")

    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_csv(self, mock_file):
        data = [{"company": "Test", "ticker": "T"}]
        gra.save_to_csv(data, "test.csv")
        mock_file.assert_called_with("test.csv", "w", newline="")

    def test_create_corporate_structure(self):
        data = [
            {"company": "A", "ticker": "A1", "sector": "Tech", "market_cap": 100, "revenue": 50},
            {"company": "B", "ticker": "B1", "sector": "Finance", "market_cap": 200, "revenue": 150},
            {"company": "C", "ticker": "C1", "sector": "Tech", "market_cap": 300, "revenue": 250},
        ]
        structure = gra.create_corporate_structure(data)
        self.assertIn("Tech", structure)
        self.assertIn("Finance", structure)
        self.assertEqual(len(structure["Tech"]), 2)
        self.assertEqual(len(structure["Finance"]), 1)

if __name__ == '__main__':
    unittest.main()
