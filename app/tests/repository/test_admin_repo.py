from app.repository.auth_repo import admin_authentication_with_email, admin_save_in_database
from app.database_models.admins_table import Admins
from unittest.mock import AsyncMock, Mock
from app.repository.weather_repo import find_top_location, find_top_user

async def test_admin_exist_in_database(db_session):
    admin = await admin_authentication_with_email(
        db_session,
        "mirha@gmail.com"
    )

    assert admin.email == "mirha@gmail.com"
    assert admin is not None

async def test_admin_save_in_database(db_session):
    new_admin = Admins(
        name = "Mirha",
        age = 23,
        phone_number = "03625252555",
        email = "mirha@gmail.com",
        password = "Beauty"
    )

    await admin_save_in_database(
        db_session,
        new_admin
    )

    result = await admin_authentication_with_email(
        db_session,
        "mirha@gmail.com"
    )

    assert result is not None
    assert result.email == "mirha@gmail.com"

async def test_top_search_location_successfully():
    mock_result = Mock()
    mock_result.first.return_value = ("Karachi", 4)

    session = AsyncMock()
    session.execute.return_value = mock_result

    result = await find_top_location(
        session
    )

    assert result == {
        "city_name": "Karachi",
        "total": 4
    }    

async def test_top_search_location_failed():
    mock_result = Mock()
    mock_result.first.return_value = None

    fake_session = AsyncMock()
    fake_session.execute.return_value = mock_result

    response = await find_top_location(
        fake_session
    )

    assert response is None


async def test_top_user_not_found():

    mock_result = Mock()
    mock_result.first.return_value = None

    fake_session = AsyncMock()
    fake_session.execute.return_value = mock_result

    response = await find_top_user(
        fake_session
    )

    assert response == None

async def test_top_user_found():

    fake_mock = Mock()
    fake_mock.first.return_value = (1, "Muhammad Khalfan", 5)

    fake_session = AsyncMock()
    fake_session.execute.return_value = fake_mock

    response = await find_top_user(fake_session)

    assert response == {
        "user_id": 1,
        "user_name": "Muhammad Khalfan",
        "total": 5
    }