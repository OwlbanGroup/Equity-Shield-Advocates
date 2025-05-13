import json

class CorporateStructureAI:
    def __init__(self, json_path='corporate_structure.json'):
        with open(json_path, 'r') as f:
            self.data = json.load(f)

    def get_sectors(self):
        """
        Return the list of sectors in the data.
        """
        return list(self.data.keys())

    def get_companies_by_sector(self, sector):
        """
        Return the list of companies for a given sector.
        """
        return self.data.get(sector, [])

    def query(self, sector):
        """
        Query method to get companies by sector.
        """
        return self.data.get(sector, "Sector not found.")

if __name__ == "__main__":
    ai = CorporateStructureAI()
    print("Sectors:")
    print(ai.get_sectors())
