from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from app.database.database_connection import get_session
from app.core.exceptions import UserAlreadyExist, ServerError, InvalidCredentials, SecretDataNotFound, InvalidToken, DatabaseError
from app.services import weather_service
from app.core.jwt import user_token
from app.services import user_history
from app.core.exceptions import HistoryNotFound

router = APIRouter()


@router.get("/get_weather", status_code=status.HTTP_200_OK)
async def get_weather(city_name: str, session: Session=Depends(get_session), user: dict=Depends(user_token)):
    try:
        result = await weather_service.get_live_weather(city_name, session, user)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return result

