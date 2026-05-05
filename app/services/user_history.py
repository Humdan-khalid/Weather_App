from app.repository import auth_repo
from sqlmodel import Session
from app.utils import caching
from app.repository import weather_repo
import json
from app.core import exceptions
from app.core.log_config import logger

def get_user_history(session: Session, user: dict):
    db_user = auth_repo.user_authentication_with_email(session, user["email"])

    if not db_user:
        logger.warning(f"Unauthorized user tried to access user history | email: {user['email']}")
        raise exceptions.InvalidCredentials("User not found!")
    
    cache = caching.get_user_weather_history_from_cache(user['id'])

    if cache:
        logger.info(f"User history was fetched from the cache. | email: {user['email']}")
        return json.loads(cache)
    
    history = weather_repo.find_user_history(session, user)

    if not history:
        logger.warning(f"user history not found! | email: {user['email']}")
        raise exceptions.HistoryNotFound("user history not found!")
    
    caching.save_history_in_cache(history, user)

    logger.info(f"User history was fetched from the database. | Email: {user['email']}")
    return history


def get_top_search_location(session: Session, admin: dict):
    db_admin = auth_repo.admin_authentication_with_email(session, admin)

    if not db_admin:
        logger.warning(f"An unauthorized admin tried to access the top searched city. | admin_email: {admin['email']}")
        raise exceptions.InvalidCredentials("Admin not found!")
    
    city = weather_repo.find_top_location(session)

    logger.info(f"Admin successfully access the top search city. | admin_email: {admin['email']}")
    return city


def get_top_data_user(session: Session, admin):
    db_admin = auth_repo.admin_authentication_with_email(session, admin['email'])

    if not db_admin:
        logger.warning(f"An unauthorized admin tried to access the top user data. | admin_email: {admin['email']}")
        raise exceptions.InvalidCredentials("Admin not found!")
    
    db_user = weather_repo.find_top_user(session)

    if not db_user:
        logger.warning("Top user data not found!")
        raise exceptions.UserNotFound("top user not found!")
    
    logger.info(f"Admin successfully access the top user data. | email: {admin['email']}")
    return db_user