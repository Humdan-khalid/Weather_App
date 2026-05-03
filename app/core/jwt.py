from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from app.utils.log_config import logger
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import secret_key, algorithm
from app.core.exceptions import SecretDataNotFound, TokenExpired, InvalidToken

def valid_jwt_config():
    if not secret_key:
        raise SecretDataNotFound("Secret key not found!")

    if not algorithm:
        raise SecretDataNotFound("Algorithm not found!")

def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=60)):
    valid_jwt_config()

    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = str(user_data["id"])
    payload["type"] = "access"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    logger.info("Token created sucessfully!")
    return token

def user_token_verification(token: str):
    valid_jwt_config()
    
    try:
        user_token = jwt.decode(token, secret_key, algorithm)
    except ExpiredSignatureError:
        raise TokenExpired("Token expired!")
    except JWTError:
        raise InvalidToken("Invalid token!")
    
    return user_token

security = HTTPBearer()

def user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    return user_token_verification(token)