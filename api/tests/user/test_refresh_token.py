from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import pytest


@pytest.fixture(scope="function")
def refresh_token_context():
    access_token = create_access_token("testuser", fresh=True)
    expired_token = create_access_token(
        "testuser", expires_delta=timedelta(seconds=-10)
    )
    refresh_token = create_refresh_token("testuser")
    not_fresh_token = create_access_token("testuser", fresh=False)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expired_token": expired_token,
        "not_fresh_token": not_fresh_token,
    }


def test_refresh_token_invalid_token(app, refresh_token_context):
    client = app.test_client()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(refresh_token_context["access_token"]),
    }
    response = client.post("/refreshToken", headers=headers)

    assert response.status_code == 401
    assert response.json["error"] == "invalid_token"


def test_refresh_token_no_token(app):
    client = app.test_client()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = client.post("/refreshToken", headers=headers)

    assert response.status_code == 401
    assert response.json["error"] == "authorization_required"


def test_refresh_token_success(app, mocker, refresh_token_context):
    client = app.test_client()
    mocker.patch("redis.Redis.get", return_value=None)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(refresh_token_context["refresh_token"]),
    }

    response = client.post("/refreshToken", headers=headers)

    assert response.status_code == 200
    assert "access_token" in response.json
