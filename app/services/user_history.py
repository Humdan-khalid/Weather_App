from app.repository import auth_repo
from sqlmodel import Session
from fastapi import HTTPException, status
from app.utils import caching
from app.repository import weather_repo
import json
from app.core import exceptions

def get_user_history(session: Session, user: dict):
    db_user = auth_repo.user_authentication_with_email(session, user["email"])

    if not db_user:
        raise exceptions.InvalidCredentials("User not found!")
    
    cache = caching.get_history_from_cache(user['id'])

    if cache:
        return json.loads(cache)
    
    history = weather_repo.find_user_history(session, user)

    if not history:
        raise exceptions.HistoryNotFound("user history not found!")
    
    caching.save_history_in_cache(history, user)
    return history


def get_top_search_location(session: Session, admin: dict):
    db_admin = auth_repo.admin_authentication_with_email(session, admin)

    if not db_admin:
        raise exceptions.InvalidCredentials("Admin not found!")
    
    city = weather_repo.find_top_location(session)
    return city


def get_top_data_user(session: Session, admin):
    db_admin = auth_repo.admin_authentication_with_email(session, admin['email'])

    if not db_admin:
        raise exceptions.InvalidCredentials("Admin not found!")
    
    db_user = weather_repo.find_top_user(session)

    if not db_user:
        raise exceptions.UserNotFound("top user not found!")
    
    return db_user