import unittest
import json
from api_server import app
from ai_component import CorporateStructureAI

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ai = CorporateStructureAI()

    def test_api_and_ai_consistency(self):
        # Test that API /api/companies/<sector> matches AI get_companies_by_sector
        sectors = self.ai.get_sectors()
        for sector in sectors:
            response = self.app.get(f'/api/companies/{sector}')
            self.assertEqual(response.status_code, 200)
            api_data = json.loads(response.data)
            ai_data = self.ai.get_companies_by_sector(sector)
            self.assertEqual(api_data, ai_data)

    def test_api_company_ticker_and_ai(self):
        # Test that API /api/company/<ticker> matches AI get_company_by_ticker
        sectors = self.ai.get_sectors()
        for sector in sectors:
            companies = self.ai.get_companies_by_sector(sector)
            for company in companies:
                ticker = company['ticker']
                response = self.app.get(f'/api/company/{ticker}')
                self.assertEqual(response.status_code, 200)
                api_data = json.loads(response.data)
                ai_data = self.ai.get_company_by_ticker(ticker)
                self.assertEqual(api_data, ai_data)

if __name__ == '__main__':
    unittest.main()
