import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from api_server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

API_KEY = "secret-api-key"
HEADERS = {"X-API-KEY": API_KEY}

def test_get_bank_account_success(client):
    response = client.get('/api/banks/citi-private-bank/account', headers=HEADERS)
    assert response.status_code == 200
    data = response.get_json()
    assert data['bank_name'] == "Citi Private Bank"
    assert 'account_number' in data
    assert 'routing_number' in data

def test_get_bank_account_not_found(client):
    response = client.get('/api/banks/nonexistent-bank/account', headers=HEADERS)
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_get_bank_account_unauthorized(client):
    response = client.get('/api/banks/citi-private-bank/account')
    assert response.status_code == 401

def test_validate_routing_success(client):
    payload = {"routing_number": "021000089"}
    response = client.post('/api/banks/validate-routing', headers=HEADERS, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['routing_number'] == "021000089"
    assert isinstance(data['valid'], bool)

def test_validate_routing_missing_param(client):
    response = client.post('/api/banks/validate-routing', headers=HEADERS, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_validate_routing_unauthorized(client):
    payload = {"routing_number": "021000089"}
    response = client.post('/api/banks/validate-routing', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 401

def test_transfer_success(client):
    payload = {
        "from_bank": "citi-private-bank",
        "to_bank": "citi-private-bank",
        "amount": 1000,
        "currency": "USD"
    }
    response = client.post('/api/banks/transfer', headers=HEADERS, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert data['amount'] == 1000

def test_transfer_missing_params(client):
    payload = {
        "from_bank": "citi-private-bank",
        "amount": 1000
    }
    response = client.post('/api/banks/transfer', headers=HEADERS, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_transfer_unauthorized(client):
    payload = {
        "from_bank": "citi-private-bank",
        "to_bank": "citi-private-bank",
        "amount": 1000,
        "currency": "USD"
    }
    response = client.post('/api/banks/transfer', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 401
