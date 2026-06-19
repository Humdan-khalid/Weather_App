from app.repository.auth_repo import user_authentication_with_email, user_save_in_database
from app.repository.weather_repo import save_weather_history
from app.database_models.users_table import Users
from app.database_models.user_data_history import UserHistory
import pytest
from datetime import datetime
from app.core.exceptions import DatabaseError
from unittest.mock import AsyncMock
from sqlmodel import select

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
        "bilal@gmail.com"
    )

    assert result is not None
    assert result.email == "bilal@gmail.com"


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


async def test_history_save(db_session):
    weather = {
                "temperature": 35.6,
                "feels_like":24.2,
                "humidity": 12,
                "wind": 32,
                "weather": "Cloudy",
                "description": "scattered clouds",
                "time": datetime.now()
                }

    result = await save_weather_history(
                db_session,
                36,
                weather,
                "Abu Dhabi"
    )

    result = await db_session.execute(
    select(UserHistory).where(UserHistory.id == 14)
    )

    history = result.scalar_one()

    assert history.id == 14

async def test_database_error(db_session):
    weather = {
                "temperature": 35.6,
                "feels_like": 24.2,
                "humidity": 12,
                "wind": 32,
                "weather": "Cloudy",
                "description": "scattered clouds",
                "time": datetime.now()
                }

    db_session.commit = AsyncMock(
    side_effect=Exception("Database down")
    )

    with pytest.raises(DatabaseError):
        await save_weather_history(
        db_session,
        36,
        weather,
        "Abu Dhabi"
    )        