import unittest
import os
from ai_report import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.report = ReportGenerator()
        self.text_file = 'test_report.txt'
        self.csv_file = 'test_report.csv'
        self.json_file = 'test_report.json'

    def tearDown(self):
        for file in [self.text_file, self.csv_file, self.json_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_generate_text_report(self):
        self.report.generate_text_report(self.text_file)
        self.assertTrue(os.path.exists(self.text_file))
        with open(self.text_file, 'r') as f:
            content = f.read()
        self.assertIn("Corporate Structure Report", content)

    def test_generate_csv_report(self):
        self.report.generate_csv_report(self.csv_file)
        self.assertTrue(os.path.exists(self.csv_file))
        with open(self.csv_file, 'r') as f:
            content = f.read()
        self.assertIn("Sector,Number of Companies", content)

    def test_generate_json_report(self):
        self.report.generate_json_report(self.json_file)
        self.assertTrue(os.path.exists(self.json_file))
        with open(self.json_file, 'r') as f:
            content = f.read()
        self.assertTrue(content.startswith("{"))

if __name__ == '__main__':
    unittest.main()
