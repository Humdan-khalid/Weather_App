from app.utils.password_hash import verify_hash_password, create_hash_password
from app.repository import auth_repo
from fastapi import HTTPException, status
from app.core.jwt import create_token
from app.database_models.users_table import CreateUsers, EmailStr, Users
from app.database_models.admins_table import CreateAdmin, Admins, LoginAdmin
from sqlmodel import Session
from app.core import exceptions

def new_account_created(user: CreateUsers, session: Session):
    db_user = auth_repo.user_authentication_with_email(session, user.email)
    
    if db_user:
        raise exceptions.UserAlreadyExist("Account already exist with this email.")
    
    new_user = Users(
    name=user.name.title(),
    age=user.age,
    phone_number=user.phone_number,
    email=user.email.lower(),
    password=create_hash_password(user.password)
    )

    try:
        auth_repo.user_save_in_database(session, new_user)

    except Exception as e:
        session.rollback()
        raise exceptions.ServerError("Internal Server Error")

    return new_user
    
def user_login(user, session: Session):
    db_user = auth_repo.user_authentication_with_email(session, user.email)
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
    if not verify_hash_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
    token = create_token(
        {
        "id": db_user.id,
        "email": db_user.email
        }
    )

    return{"access_token": token,
           "token_type": "Bearer"}

def admin_new_account_created(create_admin: CreateAdmin, session: Session):
    db_admin = auth_repo.admin_authentication_with_email(session, create_admin.email)

    if db_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exist at this email")
    
    new_admin = Admins(
        name=create_admin.name,
        age=create_admin.age,
        phone_number=create_admin.phone_number,
        email=create_admin.email,
        password=create_hash_password(create_admin.password)
    )

    try:
        auth_repo.admin_save_in_database(session, new_admin)
    except:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error!")
    
    return new_admin

def admin_login(admin: LoginAdmin ,session: Session):
    db_admin = auth_repo.admin_authentication_with_email(session, admin.email)

    if not db_admin:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Unauthorized user!")
    
    if not verify_hash_password(admin.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User!")
    
    token = create_token(
        {
            "id": db_admin.id,
            "email": db_admin.email
        }
    )

    return {
        "access_token": token,
        "token_type": "Bearer"
    }