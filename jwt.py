from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from main import HTTPException, status, Header
from log_config import logger

load_dotenv()

secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")

if not secret_key:
    logger.critical("Secret key not found!")
    raise ValueError("Secret key not found!")

if not algorithm:
    logger.critical("Algorithm not found!")
    raise ValueError("Algorithm not found!")

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired!")
    except JWTError:
        logger.critical("Jwt error!", exc_info=True)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="JWT error")
    return user_token

def user_token(token: str = Header(...)):
    token_parts = token.split()

    if len(token_parts) != 2:
        logger.critical("Invalid token style")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token style. token expected bearer.")
    
    scheme, token = token_parts

    if scheme.lower() != "bearer":
        logger.critical("scheme not equal of bearer.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token format.please use the bearer.")
    
    token_decoded = user_token_verification(token)
    return token_decoded