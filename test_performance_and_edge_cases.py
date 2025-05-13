import unittest
import time
from unittest.mock import patch, MagicMock
from ai_component import CorporateStructureAI
from api_server import app

class TestPerformanceAndEdgeCases(unittest.TestCase):

    @patch('gather_real_assets.yf.Ticker')
    def test_gather_real_assets_performance(self, mock_ticker):
        # Mock yfinance Ticker.info to return dummy data quickly
        mock_ticker.return_value.info = {
            "shortName": "Test Company",
            "sector": "Technology",
            "marketCap": 1000000,
            "totalRevenue": 500000
        }
        import gather_real_assets as gra
        start_time = time.time()
        data = gra.gather_data()
        duration = time.time() - start_time
        self.assertTrue(duration < 5, "Data gathering took too long")
        self.assertTrue(len(data) > 0)

    def test_ai_component_edge_cases(self):
        ai = CorporateStructureAI()
        # Test get_companies_by_sector with non-existent sector
        self.assertEqual(ai.get_companies_by_sector("NonExistentSector"), [])
        # Test get_company_by_ticker with invalid ticker returns 'Company not found.'
        self.assertEqual(ai.get_company_by_ticker("INVALID"), "Company not found.")

    def test_api_endpoints_edge_cases(self):
        client = app.test_client()
        # Invalid sector
        response = client.get('/api/companies/InvalidSector')
        self.assertEqual(response.status_code, 404)
        # Invalid ticker
        response = client.get('/api/company/INVALID')
        # The API returns 404 for invalid ticker, so test should expect 404
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
