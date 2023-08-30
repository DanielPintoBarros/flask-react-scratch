from flaskr.database.models.user import UserModel
from passlib.hash import pbkdf2_sha256
import flaskr.resources.user as user_resource
import pytest
import uuid

userEmail = "TesTing@test.com"
userPassword = "Test123!"
invalidPassword = "Test"
userUUID = uuid.uuid4()


@pytest.fixture(scope="module")
def userLogin():
    userLogin = UserModel(
        id=userUUID, email=userEmail.lower(), password=pbkdf2_sha256.hash(userPassword)
    )
    return userLogin


def test_login_success(app, mocker, userLogin):
    client = app.test_client()

    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userLogin)
    user_find_email_spy = mocker.spy(UserModel, "find_by_email")
    token_gen_spy = mocker.spy(user_resource, "create_access_token")
    ref_token_gen_spy = mocker.spy(user_resource, "create_refresh_token")
    hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": userEmail, "password": userPassword}
    response = client.post("/login", json=data, headers=headers)

    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.status_code == 200
    user_find_email_spy.assert_called_once_with(userEmail.lower())
    ref_token_gen_spy.assert_called_once_with(userUUID)
    token_gen_spy.assert_called_once_with(identity=userUUID, fresh=True)
    hash_password_spy.assert_called_once_with(userPassword, userLogin.password)


def test_login_invalid_password(app, mocker, userLogin):
    client = app.test_client()

    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userLogin)
    user_find_email_spy = mocker.spy(UserModel, "find_by_email")
    hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": userEmail, "password": invalidPassword}
    response = client.post("/login", json=data, headers=headers)

    assert response.status_code == 401
    user_find_email_spy.assert_called_once_with(userEmail.lower())
    hash_password_spy.assert_called_once_with(invalidPassword, userLogin.password)


def test_login_invalid_email(app, mocker):
    client = app.test_client()

    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=None)
    user_find_email_spy = mocker.spy(UserModel, "find_by_email")
    hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": userEmail, "password": userPassword}
    response = client.post("/login", json=data, headers=headers)

    assert response.status_code == 401
    user_find_email_spy.assert_called_once_with(userEmail.lower())
    hash_password_spy.assert_not_called()


def test_invalid_input_body_data(app):
    client = app.test_client()

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"randomField": 1}
    response = client.post("/login", json=data, headers=headers)

    assert response.status_code == 422
    assert "errors" in response.json.keys()

    errors = response.json["errors"]["json"]
    assert "email" in errors.keys()
    assert "password" in errors.keys()
    assert "randomField" in errors.keys()
    expectedErrors = {
        "email": "Missing data for required field.",
        "password": "Missing data for required field.",
        "randomField": "Unknown field.",
    }

    for key in expectedErrors:
        assert expectedErrors[key] == errors[key][0]
