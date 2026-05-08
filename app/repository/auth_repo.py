from app.database_models.users_table import Users, EmailStr
from app.database_models.admins_table import Admins
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession

async def user_authentication_with_email(session: AsyncSession, email: EmailStr):
    result = await session.execute(
            select(Users).where(Users.email == email)
    )

    return result.scalars().first()

async def user_save_in_database(session: AsyncSession, user: Users):
    session.add(user)
    await session.commit()
    await session.refresh(user)


def admin_save_in_database(session: Session, admin: Admins):
    session.add(admin)
    session.commit()
    session.refresh(admin)


def admin_authentication_with_email(session: Session, admin: dict):
    return session.exec(
                select(Admins)
                    .where(
                        Admins.email == admin
                    )).first()
