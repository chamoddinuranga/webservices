# price-service/tests/test_app.py

import requests

def test_get_crypto_price():
    response = requests.get("http://localhost:5001/crypto-price/BTC")
    assert response.status_code == 200
    assert "price" in response.json()
