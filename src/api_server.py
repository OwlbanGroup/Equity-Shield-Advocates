from flask import Flask, jsonify, make_response, redirect, request
import json
import os
from werkzeug.exceptions import NotFound
import logging
import re
from functools import wraps
from src.bank_communication import get_account_info, validate_routing_number, initiate_transfer

logging.basicConfig(level=logging.DEBUG)

# Simple API key for demonstration purposes
API_KEY = "secret-api-key"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-KEY')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


_corporate_structure_cache = None
_real_assets_cache = None

def load_corporate_structure():
    global _corporate_structure_cache
    if _corporate_structure_cache is not None:
        return _corporate_structure_cache
    json_path = os.path.join(os.path.dirname(__file__), '../data/corporate_structure.json')
    if not os.path.exists(json_path):
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/corporate_structure.json'))
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Data file not found: {json_path}")
    with open(json_path, 'r') as f:
        _corporate_structure_cache = json.load(f)
    return _corporate_structure_cache


def load_real_assets():
    global _real_assets_cache
    if _real_assets_cache is not None:
        return _real_assets_cache
    real_assets_file = os.path.join(os.path.dirname(__file__), '../data/real_assets_under_management.json')
    if not os.path.exists(real_assets_file):
        return []
    with open(real_assets_file, 'r') as f:
        _real_assets_cache = json.load(f)
    return _real_assets_cache


def load_corporate_data():
    corporate_data_file = os.path.join(os.path.dirname(__file__), '../data/corporate_data.json')
    if not os.path.exists(corporate_data_file):
        return {}
    with open(corporate_data_file, 'r') as f:
        return json.load(f)


def create_app():
    app = Flask(__name__)


    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.debug(f"404 error handler triggered: {error}")
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


    @app.route('/api/real-assets', methods=['GET'])
    def get_real_assets():
        data = load_real_assets()
        return jsonify(data)


    @app.route('/api/banking-info', methods=['GET'])
    def get_banking_info():
        logging.debug("get_banking_info endpoint called")
        data = load_corporate_data()
        routing_number = None
        account_number = None
        ein_number = None


        banking_arm = data.get('Fund Overview', '')
        routing_match = re.search(r'Routing Number:\s*([\d]+)', banking_arm, re.IGNORECASE)
        if routing_match:
            routing_number = routing_match.group(1)
        else:
            logging.debug("Routing number not found in Fund Overview")


        ein_match = re.search(r'EIN Number:\s*([\d\-]+)', banking_arm, re.IGNORECASE)
        if ein_match:
            ein_number = ein_match.group(1)
        else:
            logging.debug("EIN number not found in Fund Overview")


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


    @app.route('/api/banking-info-test', methods=['GET'])
    def get_banking_info_test():
        return jsonify({"status": "ok"}), 200


    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({"message": "pong"}), 200


    @app.route('/api/test-404', methods=['GET'])
    def test_404():
        raise NotFound("Test 404 error")

    # New endpoints for inter-bank communication

    @app.route('/api/banks/<bank_name>/account', methods=['GET'])
    @require_api_key
    def get_bank_account(bank_name):
        account_info = get_account_info(bank_name)
        if account_info:
            return jsonify(account_info)
        else:
            return jsonify({"error": f"Bank '{bank_name}' not found"}), 404

    @app.route('/api/banks/validate-routing', methods=['POST'])
    @require_api_key
    def validate_routing():
        data = request.get_json()
        routing_number = data.get('routing_number')
        if not routing_number:
            return jsonify({"error": "routing_number is required"}), 400
        is_valid = validate_routing_number(routing_number)
        return jsonify({"routing_number": routing_number, "valid": is_valid})

    @app.route('/api/banks/transfer', methods=['POST'])
    @require_api_key
    def transfer():
        data = request.get_json()
        from_bank = data.get('from_bank')
        to_bank = data.get('to_bank')
        amount = data.get('amount')
        currency = data.get('currency', 'USD')

        if not from_bank or not to_bank or not amount:
            return jsonify({"error": "from_bank, to_bank, and amount are required"}), 400

        transfer_result = initiate_transfer(from_bank, to_bank, amount, currency)
        return jsonify(transfer_result)


    return app


app = create_app()
