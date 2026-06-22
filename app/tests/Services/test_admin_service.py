from unittest.mock import Mock, patch, AsyncMock
import pytest
from app.core.exceptions import InvalidCredentials, DatabaseError, UserNotFound, AdminAlreadyExist
from app.services.auth_service import admin_login, admin_new_account_created
from app.database_models.admins_table import CreateAdmin
from app.services.user_history import get_top_search_location, get_top_data_user

async def test_admin_login_not_found():
    admin = Mock(
        email = "hamdan@gmail.com",
        password = "Circle343"
    )

    with patch(
        "app.repository.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value=None
        )
    ):
        with pytest.raises(
            InvalidCredentials
        ):

            await admin_login(
                admin,
                AsyncMock()
                )

async def test_admin_login_with_invalid_password():
    admin = Mock(
        email = "hamdan@gmail.com",
        password = "Circle"
    )

    fake_db_admin = Mock(
         password = "hashed_password"
    )

    with patch(
        "app.repository.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = fake_db_admin
        )
        ):
            with patch(
                 "app.services.auth_service.verify_hash_password",
                 return_value = False
            ):

                with pytest.raises(
                    InvalidCredentials
                ):

                    await admin_login(
                        admin,
                        AsyncMock()
            )


async def test_admin_successfully_login():
    admin = Mock(
        email = "hamdan@gmail.com",
        password = "Circle323"
    )

    with patch(
        "app.services.auth_service.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = admin
        )
    ):
        
        with patch(
            "app.services.auth_service.verify_hash_password",
            return_value = True
        ):
            with patch(
                "app.services.auth_service.create_token",
                return_value = "fake_token"
            ):
                
                result = await admin_login(
                    admin,
                    AsyncMock()
                )

                assert result["access_token"] == "fake_token"


async def test_admin_account_successfully_created():
    new_admin = CreateAdmin(
        name = "Huzaifa",
        age = 22,
        phone_number = "03172636172",
        email = "huzaifa@gmail.com",
        password = "Company43432"
    )

    with patch(
        "app.services.auth_service.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = None
        )
    ):
        with patch(
            "app.services.auth_service.auth_repo.admin_save_in_database"
        ):
                
            result = await admin_new_account_created(
                new_admin,
                AsyncMock()
                )

            assert result.age == 22
        

async def test_admin_already_exist():
    new_admin = CreateAdmin(
    name = "Huzaifa",
    age = 22,
    phone_number = "03172636172",
    email = "huzaifa@gmail.com",
    password = "Company43432"
    )

    with patch(
        "app.services.auth_service.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = new_admin
        )
    ):
        with pytest.raises(
            AdminAlreadyExist
        ):
            await admin_new_account_created(
                new_admin,
                AsyncMock()
            )

async def test_admin_internal_server_error():
    new_admin = CreateAdmin(
    name = "Huzaifa",
    age = 22,
    phone_number = "03172636172",
    email = "huzaifa@gmail.com",
    password = "Company43432"
    )

    fake_session = AsyncMock()    

    with patch(
        "app.services.auth_service.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = None
        )
    ):
        with patch(
            "app.services.auth_service.auth_repo.admin_save_in_database",
            new = AsyncMock(
                side_effect = DatabaseError(
                "Internal Server error"
            ))
        ):
            with pytest.raises(DatabaseError):
                await admin_new_account_created(
                    new_admin,
                    fake_session
                )

    fake_session.rollback.assert_awaited_once()


admin: dict = {
    "id": 1,
    "name": "Ahtasham",
    "email": "ahtasham@gmail.com"
}

async def test_admin_not_found():
    with patch(
        "app.services.user_history.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = None
    )
    ):
        with pytest.raises(
            InvalidCredentials
        ):
            await get_top_search_location(
                AsyncMock(),
                admin
            )


city = {
    "city": "karachi",
    "total": 5
}

async def test_get_top_search_location_run_successfully():
    with patch(
        "app.services.user_history.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = admin
        )
    ):
        with patch(
            "app.services.user_history.weather_repo.find_top_location",
            new = AsyncMock(
                return_value = city
            )
        ):

            response = await get_top_search_location(
                AsyncMock(),
                admin
            )

            assert response == city

async def test_admin_not_found():
    with patch(
        "app.services.user_history.auth_repo.admin_authentication_with_email",
         new = AsyncMock(
        return_value = None
        )

    ):
       
        with pytest.raises(
            InvalidCredentials
        ):
            response = await get_top_data_user(
            AsyncMock(),
            admin
            )

            assert response == None

async def test_top_user_not_found():
    with patch(
        "app.services.user_history.auth_repo.admin_authentication_with_email",
        new = AsyncMock(
            return_value = admin
        )
    ):
        with patch(
            "app.services.user_history.weather_repo.find_top_user",
            new = AsyncMock(
                return_value = None
            )
        ):
            
            with pytest.raises(
                UserNotFound
            ):
            
                response = await get_top_data_user(
                AsyncMock(),
                admin
                )

                assert response is None

fake_top_user = {
    "id": 1,
    "name": "Hammad"
}

async def test_top_user_find_successfully():
    with patch(
        "app.services.user_history.auth_repo.admin_authentication_with_email",
        new = AsyncMock(return_value = admin
    )
    ):
        with patch(
            "app.services.user_history.weather_repo.find_top_user",
            new = AsyncMock(
                return_value = fake_top_user
            ) 
        ):
            await get_top_data_user(
                AsyncMock(),
                admin
            )