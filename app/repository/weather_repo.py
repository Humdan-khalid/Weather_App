from sqlmodel import Session, select, func
from app.database_models.user_data_history import UserHistory
from app.database_models.user_data_history import UserHistory
from app.core import exceptions
from app.repository.auth_repo import AsyncSession
from app.core.log_config import logger
from app.database_models.users_table import Users
from sqlalchemy.exc import SQLAlchemyError

async def save_weather_history(session: AsyncSession, user_id: int, data: dict, city: str):
        user_history = UserHistory(
        user_id=int(user_id),
        city_name=city,
        temperature=float(data['temperature']),
        feels_like=float(data['feels_like']),
        humidity=int(data['humidity']),
        wind=float(data['wind']),
        weather=data['weather'],
        description=data['description'],
        time=str(data['time'])
        )

        try:
            session.add(user_history)
            await session.commit()
            await session.refresh(user_history)
            
        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception("Database error while saved the weather history.")
            raise exceptions.DatabaseError("Database error while saved the weather history.") from e


async def find_user_history(session: AsyncSession, user: dict):
    try:
        db_user_history = await session.execute(select(UserHistory).where(UserHistory.user_id == user["id"]))

        result = db_user_history.scalars().all()

        if not result:
            logger.info(f"User history not found in database. User | {user['id']}")
            raise exceptions.HistoryNotFound("user history not found!")

        user_history = [history.model_dump() for history in result]
        return user_history
    
    except SQLAlchemyError as e:
        logger.exception(f"Database error while fetching the user history. User|{user['id']}")
        raise exceptions.DatabaseError("Database error while fetching the user history.") from e 


async def find_top_location(session: AsyncSession):
        try:
            city_name = await session.execute(
                    select(UserHistory.city_name,
                           func.count().label("total")
                           )
                           .group_by(UserHistory.city_name)
                           .order_by(func.count().desc())
                            )
         
            result = city_name.first()

            if not result:
                return None

            city, total = result

            return{"city_name": city,
                "total": total}
        
        except SQLAlchemyError as e:
            logger.error(f"Database error while admin fetching the top search city.")
            raise exceptions.DatabaseError("Database error while admin fetching the top search city.") from e

async def find_top_user(session: AsyncSession):
    try:
        user = await session.execute(
            select(
                Users.id, Users.name,
                func.count(UserHistory.user_id).label("total")
            )
            .join(UserHistory, Users.id == UserHistory.user_id)
            .group_by(Users.id, Users.name)
            .order_by(func.count(UserHistory.user_id).desc())
            )
        
        result = user.first()
    
        if not result:
            return None
    
        user_id, user_name, total = result

        return{
            "user_id": user_id,
            "user_name": user_name,
            "total": total
            }
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching the top user of application")
        raise exceptions.DatabaseError("Database error while fetching the top user of application") from e

