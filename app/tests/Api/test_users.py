from unittest.mock import patch
from app.core.exceptions import UserAlreadyExist, ServerError, \
InvalidCredentials, SecretDataNotFound, InvalidToken


payload = {
        "id": 1,
        "name": "Hamdan Khalid",
        "age": 22,
        "phone_number": "03126264646",
        "email": "hamdankhalid111@gmail.com",
        "password": "Bismillah2830"
    }

def test_create_user(client):
    fake_user = payload

    with patch(
        "app.services.auth_service.new_account_created"
    ) as fake_service:
        
        fake_service.return_value = fake_user

        response = client.post(
                "/users",
                json = payload
                            )
        
        assert response.status_code == 201

        assert response.json()['phone_number'] \
        == "03126264646"

        fake_service.assert_called_once()


def test_create_user_already_exist(client):
    with patch(
        "app.services.auth_service.new_account_created"
    ) as fake_service:
        
        fake_service.side_effect = \
            UserAlreadyExist(
                "Account already exist."
            )
        
        response = client.post(
            "/users",
            json = payload                 
            )
        
        assert response.status_code == 409


def test_create_user_server_error(client):
    with patch(
        "app.services.auth_service.new_account_created"
    ) as fake_service:
        
        fake_service.side_effect = \
        ServerError(
            "Internal Server Error"
        )

        response = client.post(
            "/users", 
            json = payload
        )
        assert response.status_code == 500


def test_user_login_fail(client):
    with patch("app.services.auth_service.user_login") as fake_auth:
        fake_auth.side_effect = InvalidCredentials(
            "Invalid email or password"
        )

        response = client.post(
            "/users/login",
            json = {
                "email" : "hamdankhalid111@gmail.com",
                "password": "Haxa1232$"
                }
        )

        assert response.status_code == 401

def test_user_login_successful(client):
    with patch(
        "app.services.auth_service.user_login"
    ) as fake_auth:
        fake_auth.return_value = {
            "access_token": "fake_token",
            "token_type": "Bearer"
        }

        response = client.post(
            "/users/login",
            json = {
                "email": "hamdankhalid111@gmail.com",
                "password": "Bismillah2830"
            }
        )

        assert response.status_code == 200


def test_user_login_secret_data_not_found(client):
    with patch("app.services.auth_service.user_login") as fake_auth:
        fake_auth.side_effect = SecretDataNotFound(
            "Secret Key not found!"
        )

        response = client.post(
            "/users/login",
            json = {
                "email" : "hamdankhalid@gmail.com",
                "password": "Hello232"
                }
        )

        assert response.status_code == 500


def test_user_login_invalid_token(client):
    with patch(
        "app.services.auth_service.user_login"
    ) as fake_auth:
        
        fake_auth.side_effect = InvalidToken(
            "Invalid token!"
        )

        response = client.post(
            "/users/login",
            json = {
                "email": "hamdan@gmail.com",
                "password": "Hamdan$@ga"
            }
        )

        assert response.status_code == 409