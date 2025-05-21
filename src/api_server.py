from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import datetime
import logging
import os
from typing import Optional, Dict, List, Any
import json
from src.bank_communication import get_account_info, validate_routing_number, initiate_transfer

# Configure logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": '*',
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-API-KEY"]
    }
})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'api_'
})

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'corporate_data.json')
CORPORATE_STRUCTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'corporate_structure.json')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.path == '/health':
            return f(*args, **kwargs)
            
        api_key = request.headers.get('X-API-KEY')
        expected_key = 'equity-shield-2024-secure-key'
        
        # Debug logging
        print("\n=== API Key Debug Info ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Raw headers: {request.headers}")
        print(f"X-API-KEY header: {api_key}")
        print(f"Expected API key: {expected_key}")
        print(f"Keys match: {api_key == expected_key}")
        print(f"Key lengths - Received: {len(api_key) if api_key else 0}, Expected: {len(expected_key)}")
        print(f"Key types - Received: {type(api_key)}, Expected: {type(expected_key)}")
        print("=== End Debug Info ===\n")
        
        if not api_key:
            logger.warning(f"No API key provided in request from {get_remote_address()}")
            return jsonify({
                'status': 'error',
                'error': 'API key is required',
                'message': 'API key is required in X-API-KEY header'
            }), 401
            
        if api_key != expected_key:
            logger.warning(f"Invalid API key provided. Received: '{api_key}', Expected: '{expected_key}'")
            return jsonify({
                'status': 'error',
                'error': 'Invalid API key',
                'message': 'Invalid API key'
            }), 401
        
        logger.info(f"API key validation successful for {request.path}")
        return f(*args, **kwargs)
    return decorated_function

def load_json_file(file_path: str) -> Optional[Dict]:
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON file {file_path}: {str(e)}")
        return None

def paginate_results(data: List[Any], page: int = 1, per_page: int = 10) -> Dict:
    """Paginate a list of results"""
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(data) + per_page - 1) // per_page
    
    return {
        'data': data[start:end],
        'page': page,
        'per_page': per_page,
        'total': len(data),
        'total_pages': total_pages
    }

@app.route('/health')
@cache.cached(timeout=60)
@limiter.exempt
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Health check failed',
            'error': str(e)
        }), 500

@app.route('/api/corporate-data')
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_corporate_data():
    """Get corporate data"""
    try:
        live_data = load_json_file(DATA_FILE_PATH)
        if live_data is None:
            return jsonify({
                'status': 'error',
                'error': 'Failed to load live data',
                'message': 'Failed to load live data'
            }), 500

        corporate_summary = {
            'name': 'Equity Shield Advocates',
            'type': 'Corporation',
            'status': 'Active',
            'executive_summary': live_data.get('Executive Summary', ''),
            'fund_overview': live_data.get('Fund Overview', ''),
            'investment_strategy': live_data.get('Investment Strategy', ''),
            'team_structure': live_data.get('Team Structure', ''),
            'risk_assessment': live_data.get('Risk Assessment', ''),
            'aum': live_data.get('AUM', '')
        }
        return jsonify({'status': 'success', 'data': corporate_summary})
    except Exception as e:
        logger.error(f"Error in get_corporate_data: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'message': 'Internal server error'
        }), 500

@app.route('/api/corporate-structure')
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_corporate_structure():
    """Get corporate structure"""
    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return jsonify({
                'status': 'error',
                'error': 'Failed to load corporate structure',
                'message': 'Failed to load corporate structure'
            }), 500

        # Return empty dict if structure_data is empty
        if not structure_data:
            return jsonify({'status': 'success', 'data': {}})

        return jsonify({'status': 'success', 'data': structure_data})
    except Exception as e:
        logger.error(f"Error in get_corporate_structure: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'message': 'Internal server error'
        }), 500

@app.route('/api/companies/', defaults={'sector': None})
@app.route('/api/companies/<sector>')
@require_api_key
@cache.memoize(300)
@limiter.limit("30/minute")
def get_companies_by_sector(sector: str):
    """Get companies by sector"""
    if sector is None:
        return jsonify({
            'status': 'error',
            'error': 'Sector parameter is required',
            'message': 'Sector parameter is required'
        }), 400

    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return jsonify({
                'status': 'error',
                'error': 'Failed to load corporate structure',
                'message': 'Failed to load corporate structure'
            }), 500

        sector_data = structure_data.get(sector)
        if sector_data is None:
            return jsonify({
                'status': 'error',
                'error': f"Sector '{sector}' not found",
                'message': f"Sector '{sector}' not found"
            }), 404

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        paginated_data = paginate_results(sector_data, page, per_page)

        return jsonify({
            'status': 'success',
            'sector': sector,
            **paginated_data
        })
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': 'Invalid pagination parameters',
            'message': 'Invalid pagination parameters'
        }), 400
    except Exception as e:
        logger.error(f"Error in get_companies_by_sector: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'message': 'Internal server error'
        }), 500

@app.route('/api/company/', defaults={'ticker': None})
@app.route('/api/company/<ticker>')
@require_api_key
@cache.memoize(300)
@limiter.limit("30/minute")
def get_company_by_ticker(ticker: str):
    """Get company by ticker symbol"""
    if ticker is None:
        return jsonify({
            'status': 'error',
            'error': 'Ticker parameter is required',
            'message': 'Ticker parameter is required'
        }), 400

    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return jsonify({
                'status': 'error',
                'error': 'Failed to load corporate structure',
                'message': 'Failed to load corporate structure'
            }), 500

        for sector, companies in structure_data.items():
            for company in companies:
                if company.get('ticker', '').lower() == ticker.lower():
                    return jsonify({
                        'status': 'success',
                        'sector': sector,
                        'data': company
                    })

        return jsonify({
            'status': 'error',
            'error': f"Company with ticker '{ticker}' not found",
            'message': f"Company with ticker '{ticker}' not found"
        }), 404
    except Exception as e:
        logger.error(f"Error in get_company_by_ticker: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'message': 'Internal server error'
        }), 500

@app.route('/api/real-assets')
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_real_assets():
    """Get real assets with pagination and filtering"""
    try:
        # Get and validate pagination parameters
        page = request.args.get('page')
        per_page = request.args.get('per_page')

        # Debug logging for pagination parameters
        logger.debug(f"Received pagination parameters: page={page} ({type(page)}), per_page={per_page} ({type(per_page)})")
        
        if page is not None or per_page is not None:
            try:
                page = int(page) if page is not None else 1
                per_page = int(per_page) if per_page is not None else 10
                if page < 1 or per_page < 1:
                    raise ValueError()
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid pagination parameters',
                    'message': 'Page and per_page must be valid positive integers'
                }), 400
        else:
            page = 1
            per_page = 10

        live_data = load_json_file(DATA_FILE_PATH)
        if live_data is None:
            # Return empty result set if file doesn't exist
            return jsonify({
                'status': 'success',
                'data': [],
                'page': page,
                'per_page': per_page,
                'total': 0,
                'total_pages': 0,
                'last_updated': datetime.datetime.now().isoformat()
            })

        # Extract and prepare assets data
        assets = []
        asset_keys = ['MSFT', 'GOOG', 'JPM', 'BAC', 'C', 'PLD', 'AMT', 'SPG']
        
        # Apply filters if provided
        # Get and validate market cap filters
        try:
            min_market_cap = request.args.get('min_market_cap')
            max_market_cap = request.args.get('max_market_cap')
            min_market_cap = float(min_market_cap) if min_market_cap is not None else None
            max_market_cap = float(max_market_cap) if max_market_cap is not None else None
        except ValueError:
            return jsonify({
                'status': 'error',
                'error': 'Invalid market cap parameters',
                'message': 'Market cap filters must be valid numbers'
            }), 400

        for key in asset_keys:
            if key in live_data:
                asset_info = live_data[key]
                if isinstance(asset_info, dict):  # Ensure it's a dictionary
                    market_cap = asset_info.get('market_cap')
                    
                    # Apply market cap filters
                    if min_market_cap and (not market_cap or market_cap < min_market_cap):
                        continue
                    if max_market_cap and (not market_cap or market_cap > max_market_cap):
                        continue
                    
                    assets.append({
                        'symbol': key,
                        'market_cap': market_cap,
                        'revenue': asset_info.get('revenue'),
                        'last_updated': asset_info.get('last_updated')
                    })

        # Sort if requested
        sort_by = request.args.get('sort_by', 'symbol')
        sort_order = request.args.get('sort_order', 'asc')
        
        if sort_by in ['symbol', 'market_cap', 'revenue']:
            reverse = sort_order.lower() == 'desc'
            assets.sort(key=lambda x: (x.get(sort_by) is None, x.get(sort_by)), reverse=reverse)

        paginated_data = paginate_results(assets, page, per_page)

        return jsonify({
            'status': 'success',
            **paginated_data,
            'last_updated': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in get_real_assets: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'message': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found',
        'error': str(error)
    }), 404

@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit exceeded errors"""
    return jsonify({
        'status': 'error',
        'message': 'Rate limit exceeded',
        'error': str(error)
    }), 429

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error': str(error)
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'An unexpected error occurred',
        'error': str(error)
    }), 500

# Bank endpoints
@app.route('/api/banking-info')
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_banking_info():
    """Get banking information"""
    return jsonify({
        'routing_number': '021000021',
        'account_number': '546910413',
        'ein_number': '12-3456789'
    })

@app.route('/api/banks/<bank_name>/account')
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_bank_account(bank_name):
    """Get bank account information"""
    account_info = get_account_info(bank_name)
    if not account_info:
        return jsonify({
            'status': 'error',
            'error': f'Bank {bank_name} not found',
            'message': f'Bank {bank_name} not found'
        }), 404
    return jsonify(account_info)

@app.route('/api/banks/validate-routing', methods=['POST'])
@require_api_key
@limiter.limit("30/minute")
def validate_routing():
    """Validate a routing number"""
    data = request.get_json()
    if not data or 'routing_number' not in data:
        return jsonify({
            'status': 'error',
            'error': 'routing_number is required',
            'message': 'routing_number is required'
        }), 400
    
    routing_number = data['routing_number']
    is_valid = validate_routing_number(routing_number)
    
    return jsonify({
        'routing_number': routing_number,
        'valid': is_valid
    })

@app.route('/api/banks/transfer', methods=['POST'])
@require_api_key
@limiter.limit("30/minute")
def transfer():
    """Initiate a bank transfer"""
    data = request.get_json()
    required_fields = ['from_bank', 'to_bank', 'amount', 'currency']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'error': f'Missing required fields',
            'message': f'Required fields: {", ".join(required_fields)}'
        }), 400
    
    result = initiate_transfer(
        data['from_bank'],
        data['to_bank'],
        data['amount'],
        data['currency']
    )
    
    return jsonify(result)

if __name__ == '__main__':
    logger.info("Starting API server on port 5001...")
    app.run(host='0.0.0.0', port=5001)
