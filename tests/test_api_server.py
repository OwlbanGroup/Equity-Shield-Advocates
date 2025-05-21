import unittest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from api_server import app

class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertEqual(data['version'], '1.0.0')

    def test_get_corporate_data(self):
        """Test corporate data endpoint"""
        response = self.app.get('/api/v1/corporate-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        corporate_data = data['data']
        self.assertIn('name', corporate_data)
        self.assertIn('type', corporate_data)
        self.assertIn('status', corporate_data)
        self.assertIn('executive_summary', corporate_data)
        self.assertIn('fund_overview', corporate_data)
        self.assertIn('investment_strategy', corporate_data)

    def test_get_corporate_structure(self):
        """Test corporate structure endpoint"""
        response = self.app.get('/api/v1/corporate-structure')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        structure_data = data['data']
        self.assertIn('departments', structure_data)
        self.assertIsInstance(structure_data['departments'], list)
        # Verify specific departments
        department_names = [dept['name'] for dept in structure_data['departments']]
        self.assertIn('Quantitative Research', department_names)
        self.assertIn('Legal Protection Division', department_names)
        self.assertIn('Investment Division', department_names)

    def test_get_real_assets(self):
        """Test real assets endpoint"""
        response = self.app.get('/api/v1/real-assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIn('total_assets', data)
        self.assertIn('last_updated', data)
        assets = data['data']
        self.assertIsInstance(assets, list)
        if len(assets) > 0:
            asset = assets[0]
            self.assertIn('symbol', asset)
            self.assertIn('market_cap', asset)
            self.assertIn('revenue', asset)
            self.assertIn('last_updated', asset)

    def test_404_handling(self):
        """Test 404 error handling"""
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Resource not found')

    def test_corporate_data_no_file(self):
        """Test corporate data endpoint with missing file"""
        # Temporarily rename the data file
        original_path = app.config.get('DATA_FILE_PATH', '')
        if os.path.exists(original_path):
            temp_path = original_path + '.tmp'
            os.rename(original_path, temp_path)
            try:
                response = self.app.get('/api/v1/corporate-data')
                self.assertEqual(response.status_code, 500)
                data = json.loads(response.data)
                self.assertEqual(data['status'], 'error')
                self.assertEqual(data['message'], 'Failed to load live data')
            finally:
                # Restore the file
                os.rename(temp_path, original_path)

if __name__ == '__main__':
    unittest.main()
