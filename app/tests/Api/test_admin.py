from unittest.mock import Mock, patch, AsyncMock
from app.core.exceptions import InvalidCredentials, AdminAlreadyExist, DatabaseError
from app.database_models.admins_table import CreateAdmin

def test_admin_login_fail(client):
    with patch(
        "app.api.admins.auth_service.admin_login",
        new = AsyncMock(
            side_effect = InvalidCredentials(
                "Invalid email or password!"
            )
        )
        ):

            response = client.post(
                "/admins/login",
                json = {
                    "email": "hamdan@gmail.com",
                    "password": "Heyyeh"
                }
            )

            assert response.status_code == 401

def test_admin_login_successful(client):
    with patch(
        "app.api.admins.auth_service.admin_login",
        new = AsyncMock(
            return_value = {
                "access_token": "fake_token",
                "token_type": "Bearer"
            }
        )
    ):
        response = client.post(
            "/admins/login",
            json = {
                "email": "hamdan@gmail.com",
                "password": "Heyyeh"
            }
        )

        assert response.status_code == 200

payload = {
        "id": 1,
        "name": "Hamdan Khalid",
        "age": 22,
        "phone_number": "03126264646",
        "email": "hamdankhalid111@gmail.com",
        "password": "Bismillah2830"
    }

async def test_admin_already_exist(client):
     with patch(
          "app.api.admins.auth_service.admin_new_account_created",
          side_effect = AdminAlreadyExist(
               "Admin account already exist!"
          )
     ):
          result = client.post("/admins", 
                               json = payload)
          
          assert result.status_code == 401


async def test_admin_database_error(client):
     with patch(
          "app.api.admins.auth_service.admin_new_account_created",
          side_effect = DatabaseError(
               "Database error!"
          )
     ):
          result = client.post("/admins", 
                               json = payload)
          
          assert result.status_code == 500

  
async def test_admin_created_successfully(client):

    data = {
        "id" : 1,
        "name" : "Hamdan", 
        "age" : 22,
        "phone_number" : "03126264646",
        "email" : "hamdankhalid111@gmail.com",
        "password" : "Bismillah2830"
    }

    with patch(
          "app.api.admins.auth_service.admin_new_account_created",
          new = AsyncMock(
               return_value = data
          )
          ):

        result = client.post("/admins", 
                               json = data)
          
        assert result.status_code == 201
