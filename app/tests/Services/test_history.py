from unittest.mock import patch, AsyncMock, Mock
from app.services.user_history import get_user_history
import json
import pytest
from app.core.exceptions import InvalidCredentials, HistoryNotFound

user = {
    "id" : 2,
    "user" : "Hamdan",
    "age" : 22,
    "phone_number" : "03190286038",
    "email" : "hamdan@gmail.com",
    "password" : "Hatehh231"
}

user_history = {
    "id" : 12,
    "temperature" : "15.01",
    "weather" : "Cloudy"
}

async def test_cache_hit():
    with patch(
        "app.services.user_history.auth_repo.user_authentication_with_email",
        new = AsyncMock(
            return_value = user
            )
    ):
        with patch(
            "app.services.user_history.caching.get_user_weather_history_from_cache",
            new = AsyncMock(
                return_value = json.dumps(user_history)               
            )
        ):
            await get_user_history(
                AsyncMock(),
                user
            )

async def test_database_hit():
    with patch(
        "app.services.user_history.auth_repo.user_authentication_with_email",
        return_value = user
    ):
        with patch(
            "app.services.user_history.caching.get_user_weather_history_from_cache",
            new = AsyncMock(
                return_value = None
            )
        ):
            
            with patch("app.services.user_history.weather_repo.find_user_history",
                   return_value = user_history
        ) as mock_db:
            
                with patch(
                    "app.services.user_history.caching.save_history_in_cache",
                    return_value = user_history
                ):
                    await get_user_history(AsyncMock, user)
            
                print(mock_db.assert_called_once())

async def test_user_not_found():
    with patch(
        "app.services.user_history.auth_repo.user_authentication_with_email",
        new = AsyncMock(return_value = None)
    ):
        with pytest.raises(
            InvalidCredentials
        ):
            await get_user_history(
                AsyncMock(),
                user
            )

async def test_history_not_found():
    with patch(
        "app.services.user_history.auth_repo.user_authentication_with_email",
        return_value = user
    ):
        with patch(
            "app.services.user_history.caching.get_user_weather_history_from_cache",
            new = AsyncMock(
                return_value = None
            )
        ):
            
            with patch("app.services.user_history.weather_repo.find_user_history",
                   return_value = None
        ):
                
                with pytest.raises(
                    HistoryNotFound
                ):
            
                    await get_user_history(AsyncMock, user)
            