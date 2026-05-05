from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from app.core.log_config import logger
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import secret_key, algorithm
from app.core.exceptions import SecretDataNotFound, TokenExpired, InvalidToken

def valid_jwt_config():
    if not secret_key:
        logger.critical("JWT config error: Secret key not found!")
        raise SecretDataNotFound("Internal Server Error!")

    if not algorithm:
        logger.critical("Jwt config error: Algorithm not found!")
        raise SecretDataNotFound("Internal Server Error!")

def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=60)):
    valid_jwt_config()

    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = str(user_data["id"])
    payload["type"] = "access"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def user_token_verification(token: str):
    valid_jwt_config()
    
    try:
        user_token = jwt.decode(token, secret_key, algorithms=[algorithm])
    
    except ExpiredSignatureError:
        logger.info("Token expired")
        raise TokenExpired("Token expired!")
    
    except JWTError as e:
        logger.error(f"Jwt decode failed: {str(e)}")
        raise InvalidToken("Invalid token!")
    
    return user_token

security = HTTPBearer()

def user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    return user_token_verification(token)