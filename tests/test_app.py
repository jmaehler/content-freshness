import pytest
import json
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Content Freshness' in rv.data  # Assuming title is in HTML

def test_audit_route_no_data(client):
    rv = client.post('/audit', json={})
    assert rv.status_code == 400
    assert b'No text provided' in rv.data

def test_audit_route_direct_text(client):
    mock_result = {"status": "Green", "reasoning": "Good"}
    
    with patch('app.audit_content') as mock_audit:
        mock_audit.return_value = mock_result
        
        rv = client.post('/audit', json={"text": "Hello world"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['result'] == mock_result
        assert data['full_text'] == "Hello world"

def test_audit_route_url(client):
    mock_text = "Scraped text"
    mock_result = {"status": "Yellow", "reasoning": "Okay"}
    
    with patch('app.scrape_url') as mock_scrape, \
         patch('app.audit_content') as mock_audit:
        
        mock_scrape.return_value = mock_text
        mock_audit.return_value = mock_result
        
        rv = client.post('/audit', json={"url": "http://example.com"})
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['result'] == mock_result
        assert data['full_text'] == mock_text
