import json
from collections import Counter

class CorporateAnalysis:
    def __init__(self, json_path='corporate_structure.json'):
        with open(json_path, 'r') as f:
            self.data = json.load(f)

    def sector_summary(self):
        """
        Returns a summary of sectors with the count of companies in each sector.
        """
        sector_counts = {sector: len(companies) for sector, companies in self.data.items()}
        return sector_counts

    def top_sectors(self, top_n=5):
        """
        Returns the top N sectors by number of companies.
        """
        sector_counts = self.sector_summary()
        sorted_sectors = sorted(sector_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_sectors[:top_n]

    def company_distribution(self):
        """
        Returns the distribution of companies across all sectors.
        """
        distribution = {}
        for sector, companies in self.data.items():
            distribution[sector] = [company.get('name', 'Unknown') for company in companies]
        return distribution

if __name__ == "__main__":
    analysis = CorporateAnalysis()
    print("Sector Summary:")
    print(analysis.sector_summary())
    print("\nTop Sectors:")
    print(analysis.top_sectors())
    print("\nCompany Distribution:")
    print(analysis.company_distribution())
