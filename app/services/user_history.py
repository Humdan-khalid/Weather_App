from app.repository import auth_repo
from sqlmodel import Session
from fastapi import HTTPException, status
from app.utils import caching
from app.repository import weather_repo
import json

def get_user_history(session: Session, user: dict):
    db_user = auth_repo.user_authentication_with_email(session, user["email"])

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User!")
    
    cache = caching.get_history_from_cache(user['id'])

    if cache:
        return json.loads(cache)
    
    history = weather_repo.find_user_history(session, user)

    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History not found!")
    
    caching.save_history_in_cache(history, user)
    return history


def get_top_search_location(session: Session, admin: dict):
    db_admin = auth_repo.admin_authentication_with_email(session, admin)

    if not db_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Admin!")
    
    city = weather_repo.find_top_location(session)

    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found!")
    
    return city


def get_top_data_user(session: Session, admin):
    db_admin = auth_repo.admin_authentication_with_email(session, admin['email'])

    if not db_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized admin!")
    
    db_user = weather_repo.find_top_user(session)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return db_user