from app.database_models.users_table import Users, EmailStr
from app.database_models.admins_table import Admins
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseError
from sqlalchemy.exc import SQLAlchemyError
from app.core.log_config import logger

async def user_authentication_with_email(session: AsyncSession, email: EmailStr):
    try:
        result = await session.execute(
                select(Users).where(Users.email == email)
        )

        return result.scalars().first()

    except SQLAlchemyError as e:
        logger.exception(
            "Database error while fetching a user data. | email=%s" ,
            email
        )
        raise DatabaseError("Unable to communicate with the database.") from e

async def user_save_in_database(session: AsyncSession, user: Users):
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    
    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception("Database error while saved the user data.")
        raise DatabaseError("Failed to save user") from e


async def admin_save_in_database(session: Session, admin: Admins):
    try:

        session.add(admin)
        await session.commit()
        await session.refresh(admin)

    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception("Database error while saved the admin data.")
        raise DatabaseError("Failed to save admin") from e

async def admin_authentication_with_email(session: Session, email: EmailStr):
    try:

        result = await session.execute(
            select(Admins)
                .where(
                    Admins.email == email
                ))
        return result.scalars().first()
    
    except SQLAlchemyError as e:
        logger.exception("Database error while fetching the admin data. | email=%s")
        raise DatabaseError("Database error while fetching the admin data.") from e