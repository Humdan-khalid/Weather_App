from sqlmodel import Session, select, func
from app.database_models.user_data_history import UserHistory
from app.database_models.user_data_history import UserHistory
from app.core import exceptions
from app.repository.auth_repo import AsyncSession
from app.core.log_config import logger
from app.database_models.users_table import Users

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
        
        except Exception as e:
            await session.rollback()
            raise exceptions.DatabaseError("Internal Server Error!")


async def find_user_history(session: AsyncSession, user: dict):
     db_user_history = await session.execute(select(UserHistory).where(UserHistory.user_id == user["id"]))
     result = db_user_history.scalars().all()
     user_history = [history.model_dump() for history in result]
     return user_history

async def find_top_location(session: AsyncSession):
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

async def find_top_user(session: AsyncSession):
    # user = await session.execute(
    #     select(UserHistory.user_id,
    #            func.count().label("total")
    #            )
    #            .group_by(UserHistory.user_id)
    #            .order_by(func.count().desc())
    #         )
    
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
    
    if not user:
          return None
    
    user_id, user_name, total = result

    return{
          "user_id": user_id,
          "user_name": user_name,
          "total": total}