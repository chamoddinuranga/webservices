# user-service/tests/test_app.py

import requests

def test_register_user():
    response = requests.post("http://localhost:5000/register", json={"username": "test_user"})
    assert response.status_code == 201

def test_get_users():
    response = requests.get("http://localhost:5000/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
