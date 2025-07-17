import os
import sys
import pytest

# ------------------------------------------------------------------ #
# Import project modules (add src to path)
# ------------------------------------------------------------------ #
sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

# tests/test_api.py

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_search_messages_status():
    response = client.get("/api/search/messages?query=paracetamol")
    assert response.status_code == 200

def test_top_products_status():
    response = client.get("/api/reports/top-products?limit=5")
    assert response.status_code == 200

def test_channel_activity_status():
    response = client.get("/api/channels/lobelia4cosmetics/activity")
    assert response.status_code == 200
