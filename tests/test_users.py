from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.json().get('message') == "Hello World"

def test_create_user():
    res = client.post("/users", json={'email': 'test1@gmail.com','password': 'password'})
    assert res.json().get('email') == 'test1@gmail.com'
    assert res.status_code == 201
