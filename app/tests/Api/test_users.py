from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import UserAlreadyExist, ServerError, InvalidCredentials
import pytest

client = TestClient(app)

payload = {
        "id": 1,
        "name": "Hamdan Khalid",
        "age": 22,
        "phone_number": "03126264646",
        "email": "hamdankhalid111@gmail.com",
        "password": "Bismillah2830"
    }

def test_create_user():
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


def test_create_user_already_exist():
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


def test_create_user_server_error():
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


def test_user_login_fail():
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

        assert response.status_code == 409