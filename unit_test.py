import json
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_write_data():
    response = client.post(
        "/write_data",
        json={"phone": "+71234567890", "address": "123 Main St."}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data updated successfully"}

def test_check_data():
    response = client.get("/check_data?phone=%2B71234567890")
    assert response.status_code == 200
    assert response.json() == {"address": "123 Main St."}

def test_check_data_invalid_phone():
    response = client.get("/check_data?phone=12345")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid phone number format"}
