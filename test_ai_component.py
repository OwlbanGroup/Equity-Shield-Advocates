import unittest
from ai_component import CorporateStructureAI

class TestCorporateStructureAI(unittest.TestCase):
    def setUp(self):
        self.ai = CorporateStructureAI()

    def test_get_sectors(self):
        sectors = self.ai.get_sectors()
        self.assertIsInstance(sectors, list)
        self.assertIn('Financial Services', sectors)
        self.assertIn('Technology', sectors)

    def test_get_companies_by_sector(self):
        companies = self.ai.get_companies_by_sector('Financial Services')
        self.assertIsInstance(companies, list)
        self.assertTrue(len(companies) > 0)
        self.assertIn('company', companies[0])
        self.assertIn('ticker', companies[0])
        self.assertIn('market_cap', companies[0])
        self.assertIn('revenue', companies[0])

    def test_query_valid_sector(self):
        data = self.ai.query('Technology')
        self.assertIsInstance(data, list)

    def test_query_invalid_sector(self):
        data = self.ai.query('Nonexistent Sector')
        self.assertEqual(data, "Sector not found.")

if __name__ == '__main__':
    unittest.main()
