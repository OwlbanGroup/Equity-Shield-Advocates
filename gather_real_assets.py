import json
import csv
import yfinance as yf


# Representative companies' ticker symbols for each sector
AI_COMPANIES = ["GOOG", "MSFT", "NVDA"]  # Google, Microsoft, Nvidia as AI-related companies
BANKING_COMPANIES = ["JPM", "BAC", "C"]  # JPMorgan Chase, Bank of America, Citigroup
REAL_ESTATE_COMPANIES = ["PLD", "AMT", "SPG"]  # Prologis, American Tower, Simon Property Group (REITs)


def fetch_company_data(ticker):
    """
    Fetch company data using yfinance.
    Returns a dict with company name, sector, market cap as proxy for AUM, and revenue.
    """
    try:
        company = yf.Ticker(ticker)
        info = company.info
        name = info.get("shortName", ticker)
        sector = info.get("sector", "Unknown")
        market_cap = info.get("marketCap", 0)
        revenue = info.get("totalRevenue", 0)
        return {
            "company": name,
            "ticker": ticker,
            "sector": sector,
            "market_cap": market_cap,
            "revenue": revenue
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def gather_data():
    data = []
    for ticker in AI_COMPANIES:
        company_data = fetch_company_data(ticker)
        if company_data:
            data.append(company_data)
    for ticker in BANKING_COMPANIES:
        company_data = fetch_company_data(ticker)
        if company_data:
            data.append(company_data)
    for ticker in REAL_ESTATE_COMPANIES:
        company_data = fetch_company_data(ticker)
        if company_data:
            data.append(company_data)
    return data


def save_to_json(data, filename="real_assets_under_management.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


def save_to_csv(data, filename="real_assets_under_management.csv"):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")


def save_to_comprehensive_file(data, json_filename="comprehensive_corporate_structure.json", csv_filename="comprehensive_corporate_structure.csv"):
    save_to_json(data, json_filename)
    save_to_csv(data, csv_filename)
    print(f"Comprehensive corporate structure saved to {json_filename} and {csv_filename}")


def create_corporate_structure(data):
    """
    Create a corporate structure JSON organized by sector.
    """
    structure = {}
    for entry in data:
        sector = entry.get("sector", "Unknown")
        if sector not in structure:
            structure[sector] = []
        structure[sector].append({
            "company": entry.get("company"),
            "ticker": entry.get("ticker"),
            "market_cap": entry.get("market_cap"),
            "revenue": entry.get("revenue")
        })
    return structure


def save_corporate_structure(structure, filename="corporate_structure.json"):
    with open(filename, "w") as f:
        json.dump(structure, f, indent=4)
    print(f"Corporate structure saved to {filename}")


def main():
    data = gather_data()
    save_to_json(data)
    save_to_csv(data)
    save_to_comprehensive_file(data)
    structure = create_corporate_structure(data)
    save_corporate_structure(structure)


if __name__ == "__main__":
    main()
