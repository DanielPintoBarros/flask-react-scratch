from flaskr.database.models.user import UserModel
from flaskr.resources.user import psql
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
)
import pytest
import uuid

userEmail = "test@test.com"
userOldPassword = "Test123!"
userNewPassword = "123Test!"
userOldPasswordHashed = pbkdf2_sha256.hash(userOldPassword)
invalidPassword = "Test"
userUUID = uuid.uuid4()


@pytest.fixture()
def userModel():
    user = UserModel(
        id=userUUID,
        email=userEmail.lower(),
        password=userOldPasswordHashed,
        first_name="test",
        last_name="test",
        permission="USER",
    )
    return user


@pytest.fixture(scope="function")
def change_password_context():
    fresh_access_token = create_access_token("testuser", fresh=True)
    not_fresh_access_token_token = create_access_token("testuser", fresh=False)

    return {
        "fresh_access_token": fresh_access_token,
        "not_fresh_access_token_token": not_fresh_access_token_token,
    }


def test_not_fresh_token(app, change_password_context):
    client = app.test_client()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(
            change_password_context["not_fresh_access_token_token"]
        ),
    }

    data = {"old_password": "", "confirm_old_password": "", "new_password": ""}
    response = client.post("/changePassword", headers=headers, json=data)

    assert response.status_code == 401
    assert response.json["error"] == "fresh_token_required"


def test_success(app, mocker, userModel, change_password_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userModel)
    mocker.patch("sqlalchemy.orm.scoping.scoped_session.add", return_value=None)
    mocker.patch("sqlalchemy.orm.scoping.scoped_session.commit", return_value=None)
    user_find_id_spy = mocker.spy(UserModel, "find_by_id")
    verify_hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")
    hash_password_spy = mocker.spy(pbkdf2_sha256, "hash")
    sql_add_spy = mocker.spy(psql.session, "add")
    sql_commit_spy = mocker.spy(psql.session, "commit")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(
            change_password_context["fresh_access_token"]
        ),
    }

    data = {
        "old_password": userOldPassword,
        "confirm_old_password": userOldPassword,
        "new_password": userNewPassword,
    }
    response = client.post("/changePassword", headers=headers, json=data)

    assert response.status_code == 200
    user_find_id_spy.assert_called_once()
    verify_hash_password_spy.assert_called_once_with(
        userOldPassword, userOldPasswordHashed
    )
    hash_password_spy.assert_called_once_with(userNewPassword)
    sql_add_spy.assert_called_once_with(userModel)
    sql_commit_spy.assert_called_once()


def test_wrong_password_confirmation(app, mocker, userModel, change_password_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userModel)
    user_find_id_spy = mocker.spy(UserModel, "find_by_id")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(
            change_password_context["fresh_access_token"]
        ),
    }

    data = {
        "old_password": userOldPassword,
        "confirm_old_password": invalidPassword,
        "new_password": userNewPassword,
    }
    response = client.post("/changePassword", headers=headers, json=data)

    assert response.status_code == 400
    user_find_id_spy.assert_called_once()


def test_wrong_password(app, mocker, userModel, change_password_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userModel)
    user_find_id_spy = mocker.spy(UserModel, "find_by_id")
    verify_hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(
            change_password_context["fresh_access_token"]
        ),
    }

    data = {
        "old_password": invalidPassword,
        "confirm_old_password": invalidPassword,
        "new_password": userNewPassword,
    }
    response = client.post("/changePassword", headers=headers, json=data)

    assert response.status_code == 400
    user_find_id_spy.assert_called_once()
    verify_hash_password_spy.assert_called_once_with(
        invalidPassword, userOldPasswordHashed
    )


def test_databas_error(app, mocker, userModel, change_password_context):
    client = app.test_client()

    mocker.patch("redis.Redis.get", return_value=None)
    mocker.patch("sqlalchemy.orm.query.Query.first", return_value=userModel)
    mocker.patch("sqlalchemy.orm.scoping.scoped_session.add", return_value=None)
    mocker.patch(
        "sqlalchemy.orm.scoping.scoped_session.commit", side_effect=Exception()
    )
    user_find_id_spy = mocker.spy(UserModel, "find_by_id")
    verify_hash_password_spy = mocker.spy(pbkdf2_sha256, "verify")
    hash_password_spy = mocker.spy(pbkdf2_sha256, "hash")
    sql_add_spy = mocker.spy(psql.session, "add")
    sql_commit_spy = mocker.spy(psql.session, "commit")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(
            change_password_context["fresh_access_token"]
        ),
    }

    data = {
        "old_password": userOldPassword,
        "confirm_old_password": userOldPassword,
        "new_password": userNewPassword,
    }
    response = client.post("/changePassword", headers=headers, json=data)

    assert response.status_code == 500
    user_find_id_spy.assert_called_once()
    verify_hash_password_spy.assert_called_once_with(
        userOldPassword, userOldPasswordHashed
    )
    hash_password_spy.assert_called_once_with(userNewPassword)
    sql_add_spy.assert_called_once_with(userModel)
    sql_commit_spy.assert_called_once()
