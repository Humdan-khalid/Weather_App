from fastapi import APIRouter, Depends, status, HTTPException
from app.core.exceptions import HistoryNotFound, ServerError, InvalidCredentials, UserNotFound
from app.database.database_connection import get_session
from app.core.jwt import user_token
from app.services import user_history
from sqlmodel import Session

router = APIRouter()

@router.get("/get_user_history", status_code=status.HTTP_200_OK)
def get_history(session: Session=Depends(get_session), user: dict=Depends(user_token)):
    try:
        result = user_history.get_user_history(session, user)
    except ServerError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except HistoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return result


@router.get("/city", status_code=status.HTTP_200_OK)
def top_city(session: Session = Depends(get_session), admin: dict = Depends(user_token)):
    try:
        result = user_history.get_top_search_location(session, admin['email'])
    
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return result


@router.get("/top_user", status_code=status.HTTP_200_OK)
def get_user(session: Session = Depends(get_session), admin: dict=Depends(user_token)):
    try:
        result = user_history.get_top_data_user(session, admin)
    
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return result