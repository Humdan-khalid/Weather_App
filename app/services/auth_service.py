from app.utils.password_hash import verify_hash_password, create_hash_password
from app.repository import auth_repo
from app.core.jwt import create_token
from app.database_models.users_table import CreateUsers, Users, UsersLogin
from app.database_models.admins_table import CreateAdmin, Admins, LoginAdmin
from sqlmodel import Session
from app.core import exceptions
from app.core.log_config import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async def new_account_created(user: CreateUsers, session: AsyncSession):
    db_user = await auth_repo.user_authentication_with_email(session, user.email)
    
    if db_user:
        logger.warning(f"User account already exist at this email. | Email: {user.email}")
        raise exceptions.UserAlreadyExist("Account already exist with this email.")
    
    new_user = Users(
    name=user.name.title(),
    age=user.age,
    phone_number=user.phone_number,
    email=user.email.lower(),
    password=create_hash_password(user.password)
    )

    try:
        await auth_repo.user_save_in_database(session, new_user)

    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to save user account due to a database error! {str(e)}")
        raise exceptions.ServerError("Internal Server Error!")

    logger.info(f"User created sucessfully | user_email: {user.email}")
    return new_user
    
async def user_login(user: UsersLogin, session: AsyncSession):
    db_user = await auth_repo.user_authentication_with_email(session, user.email)
    
    if not db_user:
        logger.warning(f"Login attempt failed with wrong email | email: {user.email}")
        raise exceptions.InvalidCredentials("Invalid email or password!")
    
    if not verify_hash_password(user.password, db_user.password):
        logger.warning(f"Login attempt failed with wrong password | email: {user.email}")
        raise exceptions.InvalidCredentials("Invalid email or password!")
    
    token = create_token(
        {
        "id": db_user.id,
        "email": db_user.email
        }
    )

    logger.info(f"User authenticated successfully | user_email: {user.email}")

    return{"access_token": token,
           "token_type": "Bearer"}

async def admin_new_account_created(admin: CreateAdmin, session: AsyncSession):
    db_admin = await auth_repo.admin_authentication_with_email(session, admin.email)

    if db_admin:
        logger.warning(f"Admin account already exists at this email | email: {admin.email}")
        raise exceptions.AdminAlreadyExist("account already exists at this email")
    
    new_admin = Admins(
        name=admin.name,
        age=admin.age,
        phone_number=admin.phone_number,
        email=admin.email,
        password=create_hash_password(admin.password)
    )

    try:
        await auth_repo.admin_save_in_database(session, new_admin)
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to save admin account due to a database error!, {str(e)}")
        raise exceptions.AdminAlreadyExist("Internal server error!")
    
    logger.info(f"Successfully admin account created | email: {admin.email}")
    return new_admin

async def admin_login(admin: LoginAdmin ,session: Session):
    db_admin = await auth_repo.admin_authentication_with_email(session, admin.email)

    if not db_admin:
        logger.warning(f"Admin login attempt failed with wrong email | email: {admin.email}")
        raise exceptions.InvalidCredentials("Invalid email or password!")
    
    if not verify_hash_password(admin.password, db_admin.password):
        logger.warning(f"Invalid login attempt failed with wrong password | email: {admin.email}")
        raise exceptions.InvalidCredentials("Invalid email or password!")
    
    token = create_token(
        {
            "id": db_admin.id,
            "email": db_admin.email
        }
    )

    logger.info(f"Admin authenticated successfully | admin_email: {admin.email}")
    return {
        "access_token": token,
        "token_type": "Bearer"
    }