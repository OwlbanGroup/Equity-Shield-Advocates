import unittest
import time
import requests

class ApiPerformanceTest(unittest.TestCase):
    BASE_URL = "http://your-server-url-here/api"  # Please replace with actual server URL

    def test_corporate_structure_performance(self):
        start = time.time()
        response = requests.get(f"{self.BASE_URL}/corporate-structure")
        duration = time.time() - start
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 1.0, "Response took too long")

    def test_companies_by_sector_performance(self):
        start = time.time()
        response = requests.get(f"{self.BASE_URL}/companies/Technology")
        duration = time.time() - start
        self.assertIn(response.status_code, [200, 404])
        self.assertLess(duration, 1.0, "Response took too long")

    def test_company_by_ticker_performance(self):
        start = time.time()
        response = requests.get(f"{self.BASE_URL}/company/MSFT")
        duration = time.time() - start
        self.assertIn(response.status_code, [200, 404])
        self.assertLess(duration, 1.0, "Response took too long")

    def test_real_assets_performance(self):
        start = time.time()
        response = requests.get(f"{self.BASE_URL}/real-assets")
        duration = time.time() - start
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 1.0, "Response took too long")

if __name__ == "__main__":
    unittest.main()
