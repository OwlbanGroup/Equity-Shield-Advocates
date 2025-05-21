from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from functools import wraps
import datetime
import logging
import os
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from functools import wraps
import datetime
import logging
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,  # Cache for 5 minutes
    'CACHE_KEY_PREFIX': 'api_v1_',
    'CACHE_INCLUDE_HEADERS': True  # Include headers in cache key
})

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'corporate_data.json')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip validation for health check endpoint
        if request.path == '/health':
            return f(*args, **kwargs)
            
        api_key = request.headers.get('X-API-KEY')
        expected_key = os.getenv('API_KEY')
        
        if not expected_key:
            logger.error("API_KEY environment variable not set")
            return jsonify({
                'status': 'error',
                'message': 'Server configuration error'
            }), 500
            
        if not api_key:
            logger.warning("No API key provided in request")
            return jsonify({
                'status': 'error',
                'message': 'API key is required in X-API-KEY header'
            }), 401
            
        if api_key != expected_key:
            logger.warning(f"Invalid API key provided: {api_key[:4]}...")
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key'
            }), 401
        
        logger.info("API key validation successful")
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def validate_request():
    # Skip validation for health check endpoint
    if request.path == '/health':
        return None
        
    # Ensure all API endpoints require authentication
    if request.path.startswith('/api/'):
        api_key = request.headers.get('X-API-KEY')
        expected_key = os.getenv('API_KEY')
        
        if not expected_key:
            logger.error("API_KEY environment variable not set")
            return jsonify({
                'status': 'error',
                'message': 'Server configuration error'
            }), 500
            
        if not api_key:
            logger.warning("No API key provided in request")
            return jsonify({
                'status': 'error',
                'message': 'API key is required in X-API-KEY header'
            }), 401
            
        if api_key != expected_key:
            logger.warning(f"Invalid API key provided: {api_key[:4]}...")
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key'
            }), 401
    
    return None

def make_cache_key(*args, **kwargs):
    """Create a cache key that includes the API key"""
    return f"{request.path}:{request.headers.get('X-API-KEY', 'none')}"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,  # Cache for 5 minutes
    'CACHE_KEY_PREFIX': 'api_v1_',
    'CACHE_INCLUDE_HEADERS': True  # Include headers in cache key
})

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'corporate_data.json')

def load_live_data():
    """Load data from JSON file"""
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Failed to load live data: {str(e)}")
        return None

@app.route('/health')
@cache.cached(timeout=60)
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Health check failed',
            'error': str(e)
        }), 500

@app.route('/api/v1/corporate-data')
@require_api_key
def get_corporate_data():
    """Get corporate data"""
    try:
        live_data = load_live_data()
        if live_data is None:
            return jsonify({'status': 'error', 'message': 'Failed to load live data'}), 500

        # Extract relevant corporate data summary
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
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/v1/corporate-structure')
@require_api_key
def get_corporate_structure():
    """Get corporate structure"""
    try:
        live_data = load_live_data()
        if live_data is None:
            return jsonify({'status': 'error', 'message': 'Failed to load live data'}), 500

        # Extract team structure as corporate structure
        team_structure = {
            'departments': [
                {
                    'name': 'Quantitative Research',
                    'teams': [
                        {'name': 'FOUR ERA Algorithm Team', 'size': 6, 'role': 'PhDs'},
                        {'name': 'Data Engineering', 'size': 4, 'role': 'specialists'},
                        {'name': 'Backtesting Infrastructure', 'size': 3, 'role': 'engineers'}
                    ]
                },
                {
                    'name': 'Legal Protection Division',
                    'teams': [
                        {'name': 'Chief Legal Office', 'size': 1, 'role': 'ESA'},
                        {'name': 'Compliance', 'size': 4, 'role': 'Attorneys'},
                        {'name': 'Risk Mitigation', 'size': 3, 'role': 'Specialists'}
                    ]
                },
                {
                    'name': 'Investment Division',
                    'teams': [
                        {'name': 'Investment Committee', 'size': 5, 'role': 'members'},
                        {'name': 'AI Research', 'size': 8, 'role': 'PhDs'},
                        {'name': 'Quantitative Strategies', 'size': 6, 'role': 'analysts'}
                    ]
                }
            ]
        }
        return jsonify({'status': 'success', 'data': team_structure})
    except Exception as e:
        logger.error(f"Error in get_corporate_structure: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/v1/real-assets')
@require_api_key
def get_real_assets():
    """Get real assets"""
    try:
        live_data = load_live_data()
        if live_data is None:
            return jsonify({'status': 'error', 'message': 'Failed to load live data'}), 500

        # Extract real assets data
        assets = []
        asset_keys = ['MSFT', 'GOOG', 'JPM', 'BAC', 'C', 'PLD', 'AMT', 'SPG', 'EQH', 'OAS', 'OASPQ', 'JSEOAS']
        for key in asset_keys:
            if key in live_data:
                asset_info = live_data[key]
                assets.append({
                    'symbol': key,
                    'market_cap': asset_info.get('market_cap'),
                    'revenue': asset_info.get('revenue'),
                    'last_updated': asset_info.get('last_updated')
                })

        return jsonify({
            'status': 'success',
            'data': assets,
            'total_assets': len(assets),
            'last_updated': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in get_real_assets: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found',
        'error': str(error)
    }), 404

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

if __name__ == '__main__':
    logger.info("Starting API server on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)
