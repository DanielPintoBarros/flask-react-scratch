from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
import flaskr.resources.user as user_resource
import flaskr.app as flask_app
import pytest


@pytest.fixture(scope="function")
def logout_token_context():
    access_token = create_access_token("testuser", fresh=True)
    refresh_token = create_refresh_token("testuser")
    access_token_jti = decode_token(access_token)["jti"]
    refresh_token_jti = decode_token(refresh_token)["jti"]
    expired_token = create_access_token(
        "testuser", expires_delta=timedelta(seconds=-10)
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_jti": access_token_jti,
        "refresh_token_jti": refresh_token_jti,
        "expired_token": expired_token,
    }


def test_logout_with_revoked_token(app, mocker, logout_token_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value="0")
    redis_get_spy = mocker.spy(flask_app.redis_client, "get")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["access_token"]),
    }

    data = {"refresh_token": logout_token_context["refresh_token"]}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 401
    assert response.json["error"] == "token_revoked"
    redis_get_spy.assert_called_once_with(logout_token_context["access_token_jti"])


def test_logout_success_1(app, mocker, logout_token_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("redis.Redis.set", return_value=None)
    mocker.patch("redis.Redis.expire", return_value=None)
    redis_set_spy = mocker.spy(user_resource.redis_client, "set")
    redis_expires_spy = mocker.spy(user_resource.redis_client, "expire")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["access_token"]),
    }

    data = {"refresh_token": logout_token_context["refresh_token"]}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 200

    assert redis_set_spy.call_count == 2
    for exec in redis_set_spy.call_args_list:
        (key, value) = exec.args
        assert key in (
            logout_token_context["access_token_jti"],
            logout_token_context["refresh_token_jti"],
        )
        assert value == 0

    assert redis_expires_spy.call_count == 2
    for exec in redis_expires_spy.call_args_list:
        (key, value) = exec.args
        assert key in (
            logout_token_context["access_token_jti"],
            logout_token_context["refresh_token_jti"],
        )
        if key == logout_token_context["access_token_jti"]:
            assert value == 3600
        else:
            assert value == 2592000


def test_logout_success_2(app, mocker, logout_token_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("redis.Redis.set", return_value=None)
    mocker.patch("redis.Redis.expire", return_value=None)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["access_token"]),
    }
    data = {"refresh_token": "Bearer {}".format(logout_token_context["refresh_token"])}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 200


def test_logout_expired_token(app, logout_token_context):
    client = app.test_client()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["expired_token"]),
    }
    data = {"refresh_token": "Bearer {}".format(logout_token_context["refresh_token"])}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 401
    assert response.json["error"] == "token_expired"


def test_logout_missing_data(app, logout_token_context):
    client = app.test_client()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["access_token"]),
    }

    data = {"invalid_field": "invalid_field"}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 422

    errors = response.json["errors"]["json"]
    assert "refresh_token" in errors.keys()
    assert "invalid_field" in errors.keys()

    expectedErrors = {
        "refresh_token": "Missing data for required field.",
        "invalid_field": "Unknown field.",
    }

    for key in expectedErrors:
        assert expectedErrors[key] == errors[key][0]


def test_logout_invalid_data(app, mocker, logout_token_context):
    client = app.test_client()
    mocker.patch("redis.Redis.get", return_value=None)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(logout_token_context["access_token"]),
    }

    data = {"refresh_token": "invalid_refresh_token"}
    response = client.post("/logout", headers=headers, json=data)

    assert response.status_code == 400
    assert response.json["message"] == "refresh token not valid"
