import pytest
from jwt import decode
from app.config import settings


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user['email'], "password": test_user['password']},
    )
    assert res.status_code == 200
    login_res = res.json()
    payload = decode(login_res['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get('user_id') == test_user['id']
    assert login_res['token_type'] == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 404),
    ('test1@gmail.com', 'wrongpassword', 404),
    ('wrongemail@gmail.com', 'wrongpassword', 404),
    (None, 'password123', 422),
    ('test1@gmail.com', None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
