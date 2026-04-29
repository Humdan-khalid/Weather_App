from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.utils.log_config import logger
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from app.core.config import secret_key, algorithm

if not secret_key:
    logger.error("Secret key not found!")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

if not algorithm:
    logger.error("Algorithm not found!")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=60)):
    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = str(user_data["id"])
    payload["type"] = "access"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    logger.info("Token created sucessfully!")
    return token

def user_token_verification(token: str):
    try:
        user_token = jwt.decode(token, secret_key, algorithm)
    except ExpiredSignatureError:
        logger.warning("Token Expired!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired!")
    except JWTError:
        logger.warning("Jwt error!", exc_info=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT error")
    return user_token

security = HTTPBearer()

def user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    return user_token_verification(token)