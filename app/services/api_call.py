import httpx
from app.core.config import url, weather_api_key
from fastapi import HTTPException, status
from datetime import datetime
from app.core.config import url

async def get_weather_from_api(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={
            "q": city,
            "appid": weather_api_key,
            "units": "metric"
        })

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found!")
    
    data = response.json()

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