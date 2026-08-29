import pytest


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello World"


def test_create_user(client):
    res = client.post("/users/", json={'email': 'test1@gmail.com', 'password': 'password123'})
    new_user = res.json()
    assert new_user['email'] == 'test1@gmail.com'
    assert 'password' not in new_user
    assert res.status_code == 201


def test_create_user_duplicate_email(client, test_user):
    res = client.post("/users/", json={'email': test_user['email'], 'password': 'password123'})
    assert res.status_code == 500


@pytest.mark.parametrize("email, password", [
    ("not-an-email", "password123"),
    ("", "password123"),
])
def test_create_user_invalid_email(client, email, password):
    res = client.post("/users/", json={'email': email, 'password': password})
    assert res.status_code == 422


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    user = res.json()
    assert user['id'] == test_user['id']
    assert user['email'] == test_user['email']


def test_get_user_not_exist(client, test_user):
    res = client.get("/users/8000000")
    assert res.status_code == 404


def test_get_all_users(client, test_user, test_user2):
    res = client.get("/users/")
    assert res.status_code == 200
    emails = [u['email'] for u in res.json()]
    assert test_user['email'] in emails
    assert test_user2['email'] in emails
