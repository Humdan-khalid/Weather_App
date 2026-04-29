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
from app.core.exceptions import UserAlreadyExist


app = FastAPI()

app.middleware("http")(log_request_middleware)

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def user_new_account(user:CreateUsers, session: Session=Depends(get_session)):
    
    try:
        return auth_service.new_account_created(user, session)
    
    except UserAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@app.post("/login/users", status_code=status.HTTP_200_OK, response_model=LoginModel)
def login_users(user: UsersLogin, session: Session = Depends(get_session)):
    return auth_service.user_login(user, session)

@app.get("/live_weather", status_code=status.HTTP_200_OK)
async def get_weather(city_name: str, session: Session=Depends(get_session), user: dict=Depends(user_token)):
    result = await weather_service.get_live_weather(city_name, session, user)
    return result

@app.get("/get_user_history", status_code=status.HTTP_200_OK)
def get_history(session: Session=Depends(get_session), user: dict=Depends(user_token)):
    result = user_history.get_user_history(session, user)
    return result

@app.get("/city", status_code=status.HTTP_200_OK)
def top_city(session: Session = Depends(get_session), admin: dict = Depends(user_token)):
    result = user_history.get_top_search_location(session, admin['email'])
    return result

@app.get("/top_user", status_code=status.HTTP_200_OK)
def get_user(session: Session = Depends(get_session), admin: dict=Depends(user_token)):
    result = user_history.get_top_data_user(session, admin)
    return result

@app.post("/new_admin", status_code=status.HTTP_201_CREATED, response_model=ReadAdmin)
def admin_created(create_admin: CreateAdmin, session: Session = Depends(get_session)):
    result = auth_service.admin_new_account_created(create_admin, session)
    return result

@app.post("/login/admin", status_code=status.HTTP_200_OK)
def admin_login(admin: LoginAdmin ,session: Session = Depends(get_session)):
    result = auth_service.admin_login(admin, session)
    return result