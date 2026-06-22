from unittest.mock import Mock, patch, AsyncMock
from app.core.exceptions import InvalidCredentials, AdminAlreadyExist, DatabaseError, UserNotFound
from app.database_models.admins_table import CreateAdmin
from app.core.jwt import user_token
from app.main import app

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

def fake_admin():
     return {
     "id": 1
}

async def test_admin_not_found(client):
     app.dependency_overrides[user_token] = fake_admin
     with patch(
          "app.api.history.user_history.get_top_search_location",
          new = AsyncMock(
               side_effect = InvalidCredentials(
                    "Admin not found!"
               )
          )
     ):
          response = client.get("/city")

          assert response.status_code == 401
          app.dependency_overrides.clear()

top_city = {
     "city": "Karachi",
     "total": 9
}

async def test_find_top_location_successfully(client):
     app.dependency_overrides[user_token] = fake_admin
     with patch(
          "app.api.history.user_history.get_top_search_location",
          new = AsyncMock(
               return_value = top_city
     )
     ):
          response = client.get(
            "/city"    
          )

          assert response.status_code == 200
          app.dependency_overrides.clear()

async def test_invalid_admin(client):
     app.dependency_overrides[user_token] = fake_admin
     with patch(
          "app.api.history.user_history.get_top_data_user",
          new = AsyncMock(
               side_effect = InvalidCredentials(
                    "Admin not found"
               )
          )
     ):
          response = client.get("/top-user")

          assert response.status_code == 401
          app.dependency_overrides.clear()

async def test_top_user_not_found(client):
     app.dependency_overrides[user_token] = fake_admin
     with patch(
          "app.api.history.user_history.get_top_data_user",
          new = AsyncMock(
               side_effect = UserNotFound(
                    "Admin not found"
               )
          )
     ):
          response = client.get("/top-user")

          assert response.status_code == 404
          app.dependency_overrides.clear()

top_user = {
     "id": 1,
     "name": "Hamdan"
}

async def test_top_user_find_succcessfully(client):
     app.dependency_overrides[user_token] = fake_admin
     with patch(
          "app.api.history.user_history.get_top_data_user",
          new = AsyncMock(
               return_value = top_user
               )
     ):
          response = client.get("/top-user")

          assert response.status_code == 200
          app.dependency_overrides.clear()
