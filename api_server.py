from flask import Flask, jsonify, abort
import json

app = Flask(__name__)

def load_corporate_structure():
    with open('corporate_structure.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/api/corporate-structure', methods=['GET'])
def get_corporate_structure():
    data = load_corporate_structure()
    return jsonify(data)

@app.route('/api/companies/<sector>', methods=['GET'])
def get_companies_by_sector(sector):
    data = load_corporate_structure()
    sector_data = data.get(sector)
    if sector_data is None:
        abort(404, description=f"Sector '{sector}' not found")
    return jsonify(sector_data)

@app.route('/api/company/<ticker>', methods=['GET'])
def get_company_by_ticker(ticker):
    data = load_corporate_structure()
    for sector, companies in data.items():
        for company in companies:
            if company.get('ticker').lower() == ticker.lower():
                return jsonify(company)
    abort(404, description=f"Company with ticker '{ticker}' not found")

import os

REAL_ASSETS_FILE = 'real_assets_under_management.json'

def load_real_assets():
    if not os.path.exists(REAL_ASSETS_FILE):
        return []
    with open(REAL_ASSETS_FILE, 'r') as f:
        data = json.load(f)
    return data

@app.route('/api/real-assets', methods=['GET'])
def get_real_assets():
    data = load_real_assets()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
