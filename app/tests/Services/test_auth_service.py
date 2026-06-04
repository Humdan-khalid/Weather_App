from unittest.mock import Mock, patch, AsyncMock
from app.services.auth_service import new_account_created, user_login
import pytest
from app.core.exceptions import UserAlreadyExist, ServerError, InvalidCredentials

@pytest.mark.asyncio
async def test_new_account_created_success():
    fake_user = Mock()

    fake_user.name = "Hamdan khalid"
    fake_user.age = 20
    fake_user.phone_number = "03190286023"
    fake_user.email = "hamdankhalid126@gmail.com"
    fake_user.password = "Helloye525!!"


    fake_session = AsyncMock()

    with patch("app.services.auth_service.auth_repo.user_authentication_with_email") as fake_auth:

        fake_auth.return_value = None

        with patch("app.services.auth_service.auth_repo.user_save_in_database") as fake_save:
            result = await new_account_created(
                fake_user, fake_session
            )

            assert result.name == "Hamdan Khalid"
            assert result.email == "hamdankhalid126@gmail.com"

            fake_auth.assert_called_once()
            fake_save.assert_called_once()


@pytest.mark.asyncio
async def test_user_already_exist():
    fake_input_user = Mock()

    fake_input_user.email = "hamdan111@gmail.com"

    fake_session = AsyncMock()

    with patch("app.services.auth_service.auth_repo.user_authentication_with_email") as fake_auth:
        fake_auth.return_value = "existing user"

        with pytest.raises(
            UserAlreadyExist
        ):
            
            await new_account_created(
                fake_input_user,
                fake_session
            )

@pytest.mark.asyncio
async def test_server_error():
    fake_user = Mock()
    
    fake_user.name = "Hassan ahmad"
    fake_user.age = 22
    fake_user.phone_number = "03182838488"
    fake_user.email = "hamdankhalid111@gmail.com"
    fake_user.password = "Bismillah2830"

    fake_session = AsyncMock()

    with patch("app.services.auth_service.auth_repo.user_authentication_with_email") as fake_auth:
        fake_auth.return_value = None

        with patch("app.services.auth_service.auth_repo.user_save_in_database") as fake_save:
            fake_save.side_effect = Exception("DB failed")
            with pytest.raises(
                ServerError
            ):
                await new_account_created(
                    fake_user,
                    fake_session
                )

@pytest.mark.asyncio
async def test_login_success():
    fake_user = Mock()
    fake_session = AsyncMock()
    fake_db_user = Mock()

    fake_db_user.id = 1
    fake_db_user.phone_number = 3190286038
    fake_db_user.age = 22
    fake_db_user.email = "hamdan111@gmail.com"
    fake_db_user.password = "hashed password"
    
    fake_user.email = "hamdan111@gmail.com"
    fake_user.password = "my_password"

    with patch("app.services.auth_service.auth_repo.user_authentication_with_email") as fake_auth:
        fake_auth.return_value=fake_db_user

        with patch("app.services.auth_service.verify_hash_password") as fake_verify:
            fake_verify.return_value = True

            with patch("app.services.auth_service.create_token") as fake_token:
                fake_token.return_value = "jwt.fake_token"

                result = await user_login(
                    fake_user,
                    fake_session
                )

                assert result["access_token"] == "jwt.fake_token"

                fake_auth.assert_called_once()
                fake_verify.assert_called_once()
                fake_token.assert_called_once()
