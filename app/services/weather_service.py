from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from app.core.jwt import user_token
from app.services import api_call
from app.utils.caching import get_weather_data_from_cache
from app.repository import weather_repo
from app.repository import auth_repo 
from app.utils import caching

async def get_live_weather(city_name: str, session: Session, user: dict):
    db_user = auth_repo.user_authentication_with_email(session, user["email"])

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user!")
    
    city = city_name.title()

    cache_data = get_weather_data_from_cache(city)

    if cache_data:
        weather_repo.save_weather_history(session, db_user.id, cache_data, city)
        return cache_data
    
    data = await api_call.get_weather_from_api(city)

    caching.set_cached(city, data)

    weather_repo.save_weather_history(session, db_user.id, data, city)

    return data


    






