from fastapi import APIRouter, Depends, HTTPException, status
from app.core.exceptions import AdminAlreadyExist, DatabaseError, InvalidCredentials
from sqlmodel import Session
from app.database_models.admins_table import CreateAdmin, ReadAdmin
from app.database.database_connection import get_session
from app.services import auth_service
from app.database_models.admins_table import LoginAdmin
from app.repository.auth_repo import AsyncSession

router = APIRouter()


@router.post("/admins", status_code=status.HTTP_201_CREATED, response_model=ReadAdmin)
async def admin_created(create_admin: CreateAdmin, session: AsyncSession = Depends(get_session)):
    try:
        result = await auth_service.admin_new_account_created(create_admin, session)

    except AdminAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return result


@router.post("/admins/login", status_code=status.HTTP_200_OK)
async def admin_login(admin: LoginAdmin ,session: AsyncSession = Depends(get_session)):
    try:
        result = await auth_service.admin_login(admin, session)
    
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return result