from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from app.services import auth_service
from app.database_models.users_table import CreateUsers, ReadUser, UsersLogin
from app.core.exceptions import UserAlreadyExist, ServerError, InvalidCredentials, SecretDataNotFound, InvalidToken
from app.database.database_connection import get_session
from app.repository.auth_repo import AsyncSession

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
async def user_new_account(user:CreateUsers, session: AsyncSession=Depends(get_session)):
    try:
        return await auth_service.new_account_created(user, session)
    
    except UserAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except ServerError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.post("/users/login", status_code=status.HTTP_200_OK)
async def login_users(user: UsersLogin, session: AsyncSession = Depends(get_session)):
    try:
        return await auth_service.user_login(user, session)
    
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except SecretDataNotFound as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except InvalidToken as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

