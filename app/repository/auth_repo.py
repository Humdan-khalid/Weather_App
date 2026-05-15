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


async def admin_save_in_database(session: Session, admin: Admins):
    session.add(admin)
    await session.commit()
    await session.refresh(admin)


async def admin_authentication_with_email(session: Session, email: EmailStr):
    result = await session.execute(
                select(Admins)
                    .where(
                        Admins.email == email
                    ))
    
    return result.scalars().first()
