from unittest.mock import AsyncMock, patch
from app.main import app
from app.core.jwt import user_token
from app.core.exceptions import InvalidCredentials, CityNotFound, DatabaseError, WeatherApiKeyNotFound

def fake_user():
    return {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

def test_live_weather_api(client):
    app.dependency_overrides[user_token] = fake_user
    
    fake_weather = {
        "temp": 22,
        "weather": "Cloudy"
    }


    with patch(
        "app.services.weather_service.get_live_weather",
        new = AsyncMock(return_value=fake_weather)
    ):
        response = client.get(
            "/live-weather?city_name=karachi"
        )

        assert response.status_code == 200
        assert response.json() == fake_weather
        
    app.dependency_overrides.clear()

def test_invalid_credentials(client):
    with patch(
        "app.services.weather_service.get_live_weather",
        new = AsyncMock(
            side_effect = InvalidCredentials(
                "User not found!!"
            )
        )
    ):
        response = client.get(
            "/live-weather?city=Karachi"
            )
        
        assert response.status_code == 401

def test_city_not_found(client):
    app.dependency_overrides[user_token] = fake_user
    with patch(
        "app.services.weather_service.get_live_weather",
        new = AsyncMock(
            side_effect = CityNotFound(
                "City not found!!"
            )
        )
    ):
        response = client.get(
            "/live-weather?city_name=Lahore"
        )

    app.dependency_overrides.clear()
    assert response.status_code == 404

def test_database_error(client):
    app.dependency_overrides[user_token] = fake_user

    with patch(
        "app.services.weather_service.get_live_weather",
        new = AsyncMock(
            side_effect = DatabaseError(
                "Database failed"
            )
        )
    ):
        response = client.get(
            "/live-weather?city_name=Hagan"
        )

        app.dependency_overrides.clear()
        assert response.status_code == 500

def test_api_key_not_found(client):
    app.dependency_overrides[user_token] = fake_user

    with patch(
        "app.services.weather_service.get_live_weather",
        new = AsyncMock(
            side_effect = WeatherApiKeyNotFound(
                "API key not found!"
            )
        )
    ):
        response = client.get(
            "/live-weather?city_name=Hagan"
        )

        app.dependency_overrides.clear()
        assert response.status_code == 500