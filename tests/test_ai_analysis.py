import unittest
from ai_analysis import CorporateAnalysis

class TestCorporateAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = CorporateAnalysis()

    def test_sector_summary(self):
        summary = self.analysis.sector_summary()
        self.assertIsInstance(summary, dict)
        self.assertTrue(all(isinstance(count, int) for count in summary.values()))

    def test_top_sectors(self):
        top_sectors = self.analysis.top_sectors(top_n=3)
        self.assertIsInstance(top_sectors, list)
        self.assertTrue(len(top_sectors) <= 3)
        for sector, count in top_sectors:
            self.assertIsInstance(sector, str)
            self.assertIsInstance(count, int)

    def test_company_distribution(self):
        distribution = self.analysis.company_distribution()
        self.assertIsInstance(distribution, dict)
        for sector, companies in distribution.items():
            self.assertIsInstance(companies, list)
            for company in companies:
                self.assertIsInstance(company, str)

if __name__ == '__main__':
    unittest.main()
