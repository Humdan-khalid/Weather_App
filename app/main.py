from fastapi import FastAPI, status, Depends, HTTPException
from sqlmodel import Session
from app.database_models.users_table import CreateUsers, UsersLogin, ReadUser, LoginModel
from app.database_models.admins_table import CreateAdmin, ReadAdmin, LoginAdmin
from app.database.database_connection import get_session
from app.core.jwt import user_token
from app.services import auth_service
from app.services import weather_service
from app.services import user_history
from app.core.middleware import log_request_middleware
from app.core import exceptions

app = FastAPI()

app.middleware("http")(log_request_middleware)

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def user_new_account(user:CreateUsers, session: Session=Depends(get_session)):
    
    try:
        return auth_service.new_account_created(user, session)
    
    except exceptions.UserAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except exceptions.ServerError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/login/users", status_code=status.HTTP_200_OK, response_model=LoginModel)
def login_users(user: UsersLogin, session: Session = Depends(get_session)):
    try:
        return auth_service.user_login(user, session)
    except exceptions.InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.get("/live_weather", status_code=status.HTTP_200_OK)
async def get_weather(city_name: str, session: Session=Depends(get_session), user: dict=Depends(user_token)):
    try:
        result = await weather_service.get_live_weather(city_name, session, user)

    except exceptions.InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except exceptions.DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return result

@app.get("/get_user_history", status_code=status.HTTP_200_OK)
def get_history(session: Session=Depends(get_session), user: dict=Depends(user_token)):
    try:
        result = user_history.get_user_history(session, user)
    except exceptions.ServerError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except exceptions.HistoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return result

@app.get("/city", status_code=status.HTTP_200_OK)
def top_city(session: Session = Depends(get_session), admin: dict = Depends(user_token)):
    try:
        result = user_history.get_top_search_location(session, admin['email'])
    
    except exceptions.InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return result

@app.get("/top_user", status_code=status.HTTP_200_OK)
def get_user(session: Session = Depends(get_session), admin: dict=Depends(user_token)):
    try:
        result = user_history.get_top_data_user(session, admin)
    
    except exceptions.InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except exceptions.UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return result

@app.post("/new_admin", status_code=status.HTTP_201_CREATED, response_model=ReadAdmin)
def admin_created(create_admin: CreateAdmin, session: Session = Depends(get_session)):
    try:
        result = auth_service.admin_new_account_created(create_admin, session)

    except exceptions.AdminAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except exceptions.DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return result

@app.post("/login/admin", status_code=status.HTTP_200_OK)
def admin_login(admin: LoginAdmin ,session: Session = Depends(get_session)):
    try:
        result = auth_service.admin_login(admin, session)
    
    except exceptions.InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return result