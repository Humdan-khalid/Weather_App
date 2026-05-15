from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from app.database.database_connection import get_session
from app.core.exceptions import CityNotFound, InvalidCredentials, DatabaseError, WeatherApiKeyNotFound
from app.services import weather_service
from app.core.jwt import user_token
from app.repository.auth_repo import AsyncSession


router = APIRouter()


@router.get("/live-weather", status_code=status.HTTP_200_OK)
async def get_weather(city_name: str, session: AsyncSession=Depends(get_session), user: dict=Depends(user_token)):
    try:
        result = await weather_service.get_live_weather(city_name, session, user)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except WeatherApiKeyNotFound as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except CityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return result

