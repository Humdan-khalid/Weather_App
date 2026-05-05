import httpx
from app.core.config import url, weather_api_key
from fastapi import HTTPException, status
from datetime import datetime
from app.core.config import url
from app.core.log_config import logger
from app.core.exceptions import WeatherApiKeyNotFound

def validate_weather_api_key():
    if not weather_api_key:
        logger.critical("Weather api key is missing!")
        raise WeatherApiKeyNotFound("Internal Server error!")
    
    return weather_api_key

async def get_weather_from_api(city: str):
    async with httpx.AsyncClient() as client:

        api_key = validate_weather_api_key()
        response = await client.get(url, params={
            "q": city,
            "appid": api_key,
            "units": "metric"
        })

    if response.status_code != status.HTTP_200_OK:
        logger.warning(f"{city} not found!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found!")
    
    data = response.json()

    logger.info(f"{city} weather data fetch successfully.")

    return{
        "city": city,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "weather": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "time": datetime.now().strftime("%H:%M:%S")
    }