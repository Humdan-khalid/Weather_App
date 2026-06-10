from app.repository.auth_repo import user_authentication_with_email, user_save_in_database
from app.database_models.users_table import Users
import pytest

@pytest.mark.asyncio
async def test_email_not_found(db_session):
    result = await user_authentication_with_email(
        db_session,
        "hamdan323@gmail.com"
    )

    assert result is None

@pytest.mark.asyncio
async def test_find_user_by_email(db_session):
    result = await user_authentication_with_email(
        db_session,
        "hamdan@gmail.com"
    )

    assert result is not None
    assert result.email == "hamdan@gmail.com"


@pytest.mark.asyncio
async def test_user_save_in_database(db_session):
    new_user = Users(
        name = "Bilal",
        age = 22,
        phone_number = "03182827377",
        email = "bilal@gmail.com",
        password = "Bismillah1728"
    )

    await user_save_in_database(db_session, new_user)
    
    result = await user_authentication_with_email(
        db_session,
        "bilal@gmail.com"
    )

    assert result.email == "bilal@gmail.com"




