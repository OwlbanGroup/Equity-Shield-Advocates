"""Flask API server for Equity Shield Advocates."""

from __future__ import annotations

import datetime
import json
import logging
import os
from functools import wraps
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.bank_communication import (
    get_account_info,
    initiate_transfer,
    validate_routing_number,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-API-KEY"],
        }
    },
)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

cache = Cache(
    app,
    config={
        "CACHE_TYPE": "simple",
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_KEY_PREFIX": "api_",
    },
)

DATA_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "corporate_data.json",
)
CORPORATE_STRUCTURE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "corporate_structure.json",
)

HTTP_400 = 400
HTTP_401 = 401
HTTP_404 = 404
HTTP_500 = 500

ERROR_INTERNAL_SERVER = "Internal server error"
ERROR_FAILED_LOAD_STRUCTURE = "Failed to load corporate structure"
ERROR_INVALID_PAGINATION = "Invalid pagination parameters"


def json_error(
    status_code: int,
    error: str,
    message: Optional[str] = None,
    **extra: Any,
):
    """Create a consistent JSON error response."""
    payload: Dict[str, Any] = {
        "status": "error",
        "error": error,
        "message": message or error,
    }
    payload.update(extra)
    return jsonify(payload), status_code


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (OSError, json.JSONDecodeError) as exc:
        logger.error("Failed to load JSON file %s: %s", file_path, exc)
        return None


def paginate_results(data: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Paginate a list of results."""
    start = (page - 1) * per_page
    end = start + per_page
    total = len(data)
    total_pages = (total + per_page - 1) // per_page if per_page else 0

    return {
        "data": data[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }


def parse_positive_int(value: Optional[str], default: int, field_name: str) -> int:
    """Parse a positive integer query parameter."""
    if value is None:
        return default

    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(field_name) from exc

    if parsed < 1:
        raise ValueError(field_name)

    return parsed


def parse_optional_float(value: Optional[str], field_name: str) -> Optional[float]:
    """Parse an optional float query parameter."""
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(field_name) from exc


def require_api_key(view_function):
    """Require a valid API key header for protected endpoints."""

    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.path == "/health":
            return view_function(*args, **kwargs)

        api_key = request.headers.get("X-API-KEY")
        expected_key = os.getenv("API_KEY", "equity-shield-2024-secure-key")

        if not api_key:
            logger.warning("No API key provided in request from %s", get_remote_address())
            return json_error(
                HTTP_401,
                "API key is required",
                "API key is required in X-API-KEY header",
            )

        if api_key != expected_key:
            logger.warning("Invalid API key provided for request path %s", request.path)
            return json_error(HTTP_401, "Invalid API key", "Invalid API key")

        logger.info("API key validation successful for %s", request.path)
        return view_function(*args, **kwargs)

    return decorated_function


@app.route("/health", methods=["GET"])
@cache.cached(timeout=60)
@limiter.exempt
def health_check():
    """Health check endpoint."""
    try:
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.datetime.now().isoformat(),
                "version": "1.0.0",
            }
        )
    except (ValueError, TypeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Health check failed")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.route("/api/v1/corporate-data", methods=["GET"])
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_corporate_data():
    """Get corporate data."""
    try:
        live_data = load_json_file(DATA_FILE_PATH)
        if live_data is None:
            return json_error(
                HTTP_500,
                "Failed to load live data",
                "Failed to load live data",
            )

        corporate_summary = {
            "name": "Equity Shield Advocates",
            "type": "Corporation",
            "status": "Active",
            "executive_summary": live_data.get("Executive Summary", ""),
            "fund_overview": live_data.get("Fund Overview", ""),
            "investment_strategy": live_data.get("Investment Strategy", ""),
            "team_structure": live_data.get("Team Structure", ""),
            "risk_assessment": live_data.get("Risk Assessment", ""),
            "aum": live_data.get("AUM", ""),
        }
        return jsonify({"status": "success", "data": corporate_summary})
    except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Error in get_corporate_data")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.route("/api/v1/corporate-structure", methods=["GET"])
@app.route("/api/corporate-structure", methods=["GET"])
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_corporate_structure():
    """Get corporate structure."""
    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return json_error(
                HTTP_500,
                ERROR_FAILED_LOAD_STRUCTURE,
                ERROR_FAILED_LOAD_STRUCTURE,
            )

        if not structure_data:
            return jsonify({"status": "success", "data": {}})

        return jsonify({"status": "success", "data": structure_data})
    except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Error in get_corporate_structure")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.route("/api/companies/", defaults={"sector": None}, methods=["GET"])
@app.route("/api/companies/<sector>", methods=["GET"])
@require_api_key
@cache.memoize(300)
@limiter.limit("30/minute")
def get_companies_by_sector(sector: Optional[str]):
    """Get companies by sector."""
    if sector is None:
        return json_error(
            HTTP_400,
            "Sector parameter is required",
            "Sector parameter is required",
        )

    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return json_error(
                HTTP_500,
                ERROR_FAILED_LOAD_STRUCTURE,
                ERROR_FAILED_LOAD_STRUCTURE,
            )

        sector_data = structure_data.get(sector)
        if sector_data is None:
            return json_error(
                HTTP_404,
                f"Sector '{sector}' not found",
                f"Sector '{sector}' not found",
            )

        page = parse_positive_int(request.args.get("page"), 1, "page")
        per_page = parse_positive_int(request.args.get("per_page"), 10, "per_page")
        paginated_data = paginate_results(sector_data, page, per_page)

        return jsonify({"status": "success", "sector": sector, **paginated_data})
    except ValueError:
        return json_error(
            HTTP_400,
            ERROR_INVALID_PAGINATION,
            "Page and per_page must be valid positive integers",
        )
    except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Error in get_companies_by_sector")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.route("/api/company/", defaults={"ticker": None}, methods=["GET"])
@app.route("/api/company/<ticker>", methods=["GET"])
@require_api_key
@cache.memoize(300)
@limiter.limit("30/minute")
def get_company_by_ticker(ticker: Optional[str]):
    """Get company by ticker symbol."""
    if ticker is None:
        return json_error(
            HTTP_400,
            "Ticker parameter is required",
            "Ticker parameter is required",
        )

    try:
        structure_data = load_json_file(CORPORATE_STRUCTURE_PATH)
        if structure_data is None:
            return json_error(
                HTTP_500,
                ERROR_FAILED_LOAD_STRUCTURE,
                ERROR_FAILED_LOAD_STRUCTURE,
            )

        for sector, companies in structure_data.items():
            for company in companies:
                if company.get("ticker", "").lower() == ticker.lower():
                    return jsonify(
                        {
                            "status": "success",
                            "sector": sector,
                            "data": company,
                        }
                    )

        return json_error(
            HTTP_404,
            f"Company with ticker '{ticker}' not found",
            f"Company with ticker '{ticker}' not found",
        )
    except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Error in get_company_by_ticker")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.route("/api/v1/real-assets", methods=["GET"])
@app.route("/api/real-assets", methods=["GET"])
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_real_assets():
    """Get real assets with pagination and filtering."""
    try:
        page = parse_positive_int(request.args.get("page"), 1, "page")
        per_page = parse_positive_int(request.args.get("per_page"), 10, "per_page")

        logger.debug(
            "Received pagination parameters: page=%s, per_page=%s",
            page,
            per_page,
        )

        min_market_cap = parse_optional_float(
            request.args.get("min_market_cap"),
            "min_market_cap",
        )
        max_market_cap = parse_optional_float(
            request.args.get("max_market_cap"),
            "max_market_cap",
        )

        live_data = load_json_file(DATA_FILE_PATH)
        if live_data is None:
            return jsonify(
                {
                    "status": "success",
                    "data": [],
                    "page": page,
                    "per_page": per_page,
                    "total": 0,
                    "total_pages": 0,
                    "last_updated": datetime.datetime.now().isoformat(),
                }
            )

        assets: List[Dict[str, Any]] = []
        asset_keys = ["MSFT", "GOOG", "JPM", "BAC", "C", "PLD", "AMT", "SPG"]

        for key in asset_keys:
            asset_info = live_data.get(key)
            if not isinstance(asset_info, dict):
                continue

            market_cap = asset_info.get("market_cap")
            if min_market_cap is not None and (
                market_cap is None or market_cap < min_market_cap
            ):
                continue
            if max_market_cap is not None and (
                market_cap is None or market_cap > max_market_cap
            ):
                continue

            assets.append(
                {
                    "symbol": key,
                    "market_cap": market_cap,
                    "revenue": asset_info.get("revenue"),
                    "last_updated": asset_info.get("last_updated"),
                }
            )

        sort_by = request.args.get("sort_by", "symbol")
        sort_order = request.args.get("sort_order", "asc")

        if sort_by in {"symbol", "market_cap", "revenue"}:
            reverse = sort_order.lower() == "desc"
            assets.sort(
                key=lambda item: (item.get(sort_by) is None, item.get(sort_by)),
                reverse=reverse,
            )

        paginated_data = paginate_results(assets, page, per_page)

        return jsonify(
            {
                "status": "success",
                **paginated_data,
                "last_updated": datetime.datetime.now().isoformat(),
            }
        )
    except ValueError:
        return json_error(
            HTTP_400,
            ERROR_INVALID_PAGINATION,
            "Page, per_page, min_market_cap, and max_market_cap must be valid numbers",
        )
    except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback
        logger.exception("Error in get_real_assets")
        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(
        {
            "status": "error",
            "message": "Resource not found",
            "error": str(error),
        }
    ), 404


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit exceeded errors."""
    return jsonify(
        {
            "status": "error",
            "message": "Rate limit exceeded",
            "error": str(error),
        }
    ), 429


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify(
        {
            "status": "error",
            "message": ERROR_INTERNAL_SERVER,
            "error": str(error),
        }
    ), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all other exceptions."""
    logger.exception("Unhandled exception")
    return jsonify(
        {
            "status": "error",
            "message": "An unexpected error occurred",
            "error": str(error),
        }
    ), 500


@app.route("/api/banking-info", methods=["GET"])
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_banking_info():
    """Get banking information."""
    return jsonify(
        {
            "routing_number": "021000021",
            "account_number": "546910413",
            "ein_number": "12-3456789",
        }
    )


@app.route("/api/banks/<bank_name>/account", methods=["GET"])
@require_api_key
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_bank_account(bank_name):
    """Get bank account information."""
    account_info = get_account_info(bank_name)
    if not account_info:
        return json_error(
            HTTP_404,
            f"Bank {bank_name} not found",
            f"Bank {bank_name} not found",
        )
    return jsonify(account_info)


@app.route("/api/banks/validate-routing", methods=["POST"])
@require_api_key
@limiter.limit("30/minute")
def validate_routing():
    """Validate a routing number."""
    data = request.get_json(silent=True)
    if not data or "routing_number" not in data:
        return json_error(
            HTTP_400,
            "routing_number is required",
            "routing_number is required",
        )

    routing_number = data["routing_number"]
    is_valid = validate_routing_number(routing_number)

    return jsonify({"routing_number": routing_number, "valid": is_valid})


@app.route("/api/banks/transfer", methods=["POST"])
@require_api_key
@limiter.limit("30/minute")
def transfer():
    """Initiate a bank transfer."""
    data = request.get_json(silent=True)
    required_fields = ["from_bank", "to_bank", "amount", "currency"]

    if not data or not all(field in data for field in required_fields):
        return json_error(
            HTTP_400,
            "Missing required fields",
            f'Required fields: {", ".join(required_fields)}',
        )

    result = initiate_transfer(
        data["from_bank"],
        data["to_bank"],
        data["amount"],
        data["currency"],
    )
    return jsonify(result)


if __name__ == "__main__":
    logger.info("Starting API server on port 5001...")
    app.run(host=os.getenv("API_HOST", "127.0.0.1"), port=5001)
