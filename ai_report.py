import json
import csv
from ai_analysis import CorporateAnalysis

class ReportGenerator:
    def __init__(self, json_path='corporate_structure.json'):
        self.analysis = CorporateAnalysis(json_path)

    def generate_text_report(self, filename='report.txt'):
        sector_summary = self.analysis.sector_summary()
        top_sectors = self.analysis.top_sectors()
        with open(filename, 'w') as f:
            f.write("Corporate Structure Report\n")
            f.write("=========================\n\n")
            f.write("Sector Summary:\n")
            for sector, count in sector_summary.items():
                f.write(f"- {sector}: {count} companies\n")
            f.write("\nTop Sectors:\n")
            for sector, count in top_sectors:
                f.write(f"- {sector}: {count} companies\n")

    def generate_csv_report(self, filename='report.csv'):
        sector_summary = self.analysis.sector_summary()
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Sector', 'Number of Companies'])
            for sector, count in sector_summary.items():
                writer.writerow([sector, count])

    def generate_json_report(self, filename='report.json'):
        sector_summary = self.analysis.sector_summary()
        with open(filename, 'w') as f:
            json.dump(sector_summary, f, indent=4)

if __name__ == "__main__":
    report = ReportGenerator()
    report.generate_text_report()
    report.generate_csv_report()
    report.generate_json_report()
