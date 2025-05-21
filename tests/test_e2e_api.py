import unittest
import json
from unittest.mock import patch
from src.api_server import app

class EndToEndApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {'X-API-KEY': 'equity-shield-2024-secure-key'}

    def test_corporate_structure_flow(self):
        # Get corporate structure
        response = self.app.get('/api/corporate-structure', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        structure = json.loads(response.data)
        self.assertIsInstance(structure, dict)

        # For each sector, get companies and then company details
        for sector in structure.keys():
            response = self.app.get(f'/api/companies/{sector}', headers=self.headers)
            if response.status_code == 200:
                companies = json.loads(response.data)
                self.assertIsInstance(companies, list)
                for company in companies:
                    ticker = company.get('ticker')
                    if ticker:
                        response = self.app.get(f'/api/company/{ticker}', headers=self.headers)
                        self.assertIn(response.status_code, [200, 404])
                        if response.status_code == 200:
                            company_detail = json.loads(response.data)
                            self.assertIsInstance(company_detail, dict)

    @patch('src.api_server.load_json_file')
    def test_real_assets_endpoint(self, mock_load):
        mock_data = {
            'MSFT': {'market_cap': 1000, 'revenue': 500, 'last_updated': '2023-01-01'},
            'GOOG': {'market_cap': 2000, 'revenue': 800, 'last_updated': '2023-01-01'}
        }
        mock_load.return_value = mock_data
        response = self.app.get('/api/real-assets', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('data', data)

    def test_banking_info_endpoint(self):
        response = self.app.get('/api/banking-info', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('routing_number', data)
        self.assertIn('account_number', data)
        self.assertIn('ein_number', data)

    def test_invalid_endpoints(self):
        # Invalid sector
        response = self.app.get('/api/companies/InvalidSector', headers=self.headers)
        self.assertEqual(response.status_code, 404)

        # Invalid ticker
        response = self.app.get('/api/company/INVALID', headers=self.headers)
        self.assertEqual(response.status_code, 404)

        # Empty sector
        response = self.app.get('/api/companies/', headers=self.headers)
        self.assertEqual(response.status_code, 400)

        # Empty ticker
        response = self.app.get('/api/company/', headers=self.headers)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
