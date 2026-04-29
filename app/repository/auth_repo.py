from app.database_models.users_table import Users, EmailStr
from app.database_models.admins_table import Admins
from sqlmodel import Session, select

def user_authentication_with_email(session: Session, email: EmailStr):
    return session.exec(
            select(Users).where(Users.email == email)
    ).first()

def user_save_in_database(session: Session, user: Users):
    session.add(user)
    session.commit()
    session.refresh(user)


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
