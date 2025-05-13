import unittest
import json
from api_server import app

class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_corporate_structure(self):
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Financial Services', data)
        self.assertIn('Technology', data)
        self.assertIn('Real Estate', data)
        self.assertIn('Communication Services', data)

    def test_get_companies_by_sector_valid(self):
        response = self.app.get('/api/companies/Technology')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(any(company['ticker'] == 'MSFT' for company in data))

    def test_get_companies_by_sector_invalid(self):
        response = self.app.get('/api/companies/NonexistentSector')
        self.assertEqual(response.status_code, 404)

    def test_get_company_by_ticker_valid(self):
        response = self.app.get('/api/company/MSFT')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['ticker'], 'MSFT')

    def test_get_company_by_ticker_invalid(self):
        response = self.app.get('/api/company/INVALID')
        self.assertEqual(response.status_code, 404)

    def test_get_real_assets(self):
        response = self.app.get('/api/real-assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(any(asset['ticker'] == 'MSFT' for asset in data))

if __name__ == '__main__':
    unittest.main()
