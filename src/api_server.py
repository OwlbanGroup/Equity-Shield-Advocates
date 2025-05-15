from flask import Flask, jsonify, abort, make_response
import json
import os
from werkzeug.exceptions import NotFound
from flask import redirect

app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(404)
def not_found_error(error):
    app.logger.debug(f"404 error handler triggered: {error}")
    # Return JSON response for 404 errors instead of default HTML
    # Check if error is a Werkzeug NotFound exception to customize message
    message = str(error)
    if hasattr(error, 'description'):
        message = error.description
    response = make_response(jsonify({"error": message}), 404)
    app.logger.debug(f"Response content: {response.get_data(as_text=True)}")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error"}), 500

def load_corporate_structure():
    json_path = os.path.join(os.path.dirname(__file__), '../data/corporate_structure.json')
    if not os.path.exists(json_path):
        # fallback to absolute path if relative path fails
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/corporate_structure.json'))
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Data file not found: {json_path}")
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

@app.route('/api/corporate-structure', methods=['GET'])
def get_corporate_structure():
    data = load_corporate_structure()
    return jsonify(data)

@app.route('/api/companies', methods=['GET'])
def get_companies_redirect():
    return redirect('/api/companies/', code=307)

@app.route('/api/companies/', methods=['GET'])
def get_companies_by_sector_empty():
    return jsonify({"error": "Sector parameter is required"}), 400

@app.route('/api/companies/<sector>', methods=['GET'])
def get_companies_by_sector(sector):
    data = load_corporate_structure()
    if not sector:
        return jsonify({"error": "Sector parameter is required"}), 400
    sector_data = data.get(sector)
    if sector_data is None:
        return jsonify({"error": f"Sector '{sector}' not found"}), 404
    return jsonify(sector_data)

@app.route('/api/company', methods=['GET'])
def get_company_redirect():
    return redirect('/api/company/', code=307)

@app.route('/api/company/', methods=['GET'])
def get_company_by_ticker_empty():
    return jsonify({"error": "Ticker parameter is required"}), 400

@app.route('/api/company/<ticker>', methods=['GET'])
def get_company_by_ticker(ticker):
    data = load_corporate_structure()
    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400
    for sector, companies in data.items():
        for company in companies:
            if company.get('ticker').lower() == ticker.lower():
                return jsonify(company)
    return jsonify({"error": f"Company with ticker '{ticker}' not found"}), 404

REAL_ASSETS_FILE = os.path.join(os.path.dirname(__file__), '../data/real_assets_under_management.json')

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

import os
import json
from flask import jsonify

CORPORATE_DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/corporate_data.json')

def load_corporate_data():
    if not os.path.exists(CORPORATE_DATA_FILE):
        return {}
    with open(CORPORATE_DATA_FILE, 'r') as f:
        return json.load(f)

import logging

@app.route('/api/banking-info', methods=['GET'])
def get_banking_info():
    logging.debug("get_banking_info endpoint called")
    data = load_corporate_data()
    routing_number = None
    account_number = None
    ein_number = None

    import re

    # Extract routing number for Capetain Cetriva
    banking_arm = data.get('Fund Overview', '')
    routing_match = re.search(r'Routing Number:\s*([\d]+)', banking_arm, re.IGNORECASE)
    if routing_match:
        routing_number = routing_match.group(1)
    else:
        logging.debug("Routing number not found in Fund Overview")

    # Extract EIN number
    ein_match = re.search(r'EIN Number:\s*([\d\-]+)', banking_arm, re.IGNORECASE)
    if ein_match:
        ein_number = ein_match.group(1)
    else:
        logging.debug("EIN number not found in Fund Overview")

    # Extract account number for David Leeper
    executive_summary = data.get('Executive Summary', '')
    account_match = re.search(r'Account Number:\s*([\d]+)', executive_summary, re.IGNORECASE)
    if account_match:
        account_number = account_match.group(1)
    else:
        logging.debug("Account number not found in Executive Summary")

    return jsonify({
        'routing_number': routing_number,
        'account_number': account_number,
        'ein_number': ein_number
    })

@app.route('/api/test-404', methods=['GET'])
def test_404():
    raise NotFound("Test 404 error")

if __name__ == '__main__':
    app.run(debug=True)
