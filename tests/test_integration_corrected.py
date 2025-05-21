import unittest
import json
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api_server import app


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {'X-API-KEY': 'equity-shield-2024-secure-key'}

    def test_full_corporate_structure_flow(self):
        response = self.app.get('/api/corporate-structure', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        sectors = list(data.keys())
        if sectors:
            sector = sectors[0]
            response = self.app.get(f'/api/companies/{sector}', headers=self.headers)
            self.assertIn(response.status_code, [200, 404])
            if response.status_code == 200:
                companies = json.loads(response.data)
                self.assertIsInstance(companies, list)
                if companies:
                    ticker = companies[0].get('ticker')
                    if ticker:
                        response = self.app.get(f'/api/company/{ticker}', headers=self.headers)
                        self.assertIn(response.status_code, [200, 404])
                        if response.status_code == 200:
                            company = json.loads(response.data)
                            self.assertIsInstance(company, dict)

    def test_real_assets_flow(self):
        response = self.app.get('/api/real-assets', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)
        self.assertIn('total_pages', data)

    @patch('src.api_server.load_json_file')
    def test_edge_case_empty_corporate_structure(self, mock_load):
        mock_load.return_value = {}
        response = self.app.get('/api/corporate-structure', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data'], {})

    def test_edge_case_invalid_sector(self):
        response = self.app.get('/api/companies/InvalidSector', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        try:
            data = json.loads(response.get_data(as_text=True))
            self.assertIn('error', data)
        except Exception as e:
            print("Response data:", response.get_data(as_text=True))
            print("Exception:", e)
            self.fail("Response is not valid JSON or missing 'error' key")

    def test_edge_case_invalid_ticker(self):
        response = self.app.get('/api/company/INVALID', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        try:
            data = json.loads(response.get_data(as_text=True))
            self.assertIn('error', data)
        except Exception as e:
            print("Response data:", response.get_data(as_text=True))
            print("Exception:", e)
            self.fail("Response is not valid JSON or missing 'error' key")

    def test_edge_case_empty_sector(self):
        response = self.app.get('/api/companies/', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_edge_case_empty_ticker(self):
        response = self.app.get('/api/company/', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_banking_info(self):
        response = self.app.get('/api/banking-info', headers=self.headers)
        print(f"DEBUG: /api/banking-info response status: {response.status_code}")
        print(f"DEBUG: /api/banking-info response data: {response.data.decode('utf-8')}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('routing_number', data)
        self.assertIn('account_number', data)
        self.assertIn('ein_number', data)
        self.assertEqual(data['routing_number'], '021000021')
        self.assertEqual(data['account_number'], '546910413')
        self.assertEqual(data['ein_number'], '12-3456789')

if __name__ == '__main__':
    unittest.main()
