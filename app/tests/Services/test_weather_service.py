from unittest.mock import AsyncMock, patch, Mock
from app.services.weather_service import get_live_weather
from app.core.exceptions import InvalidCredentials
import pytest
from app.services.weather_service import get_live_weather

@patch(
    "app.repository.auth_repo.user_authentication_with_email"
)

@pytest.mark.asyncio
async def test_user_not_found(mock_auth):
    mock_auth.return_value = None

    with pytest.raises(
        InvalidCredentials
    ):
        await get_live_weather(
            "Karachi",
            AsyncMock(),
            {"email": "hamdan@gmail.com"}
        )

@patch(
    "app.services.weather_service.auth_repo.user_authentication_with_email"
)

@patch(
    "app.services.weather_service.get_weather_data_from_cache"
)

@patch(
    "app.services.weather_service.api_call.get_weather_from_api"
)

@patch(
    "app.services.weather_service.weather_repo.save_weather_history"
)

@pytest.mark.asyncio
async def test_cache_hit(
    fake_history,
    mock_api,
    mock_cache,
    mock_auth
    ):

    fake_user = Mock()

    fake_user.id = 1

    mock_auth.return_value = fake_user

    fake_cache = {
        "temperature": 22,
        "weather": "cloudy"
    }

    mock_cache.return_value = fake_cache

    result = await get_live_weather(
        "Karachi",
        AsyncMock(),
        {
            "email": "hamdan@gmail.com"
        }
    )
    
    assert result == fake_cache
    mock_api.assert_not_awaited()

@patch(
        "app.services.weather_service.weather_repo.save_weather_history"
)

@patch(
    "app.services.weather_service.caching.set_cached"
)

@patch(
        "app.services.weather_service.api_call.get_weather_from_api"
)

@patch(
        "app.services.weather_service.get_weather_data_from_cache"
)

@patch(
        "app.services.weather_service.auth_repo.user_authentication_with_email"
)


@pytest.mark.asyncio
async def test_weather_api_hit(
        fake_auth,
        fake_cache,
        fake_weather_api,
        fake_save_cache,
        fake_data_save
        ):
    
    fake_user = Mock()

    fake_user.id = 1

    fake_auth.return_value = fake_user

    fake_cache.return_value = None

    weather = {
        "temperature": "33",
        "weather": "Cloudy"
    }

    fake_weather_api.return_value = weather
    fake_cache.return_value = weather

    result = await get_live_weather(
        "Lahore",
        AsyncMock(),
        {
            "email": "hamdan@gmail.com"
        } 
    )

    assert result == weather