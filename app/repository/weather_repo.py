from sqlmodel import Session, select, func
from app.database_models.user_data_history import UserHistory
from fastapi import HTTPException, status
from app.database_models.user_data_history import UserHistory

def save_weather_history(session: Session, user_id: int, data: dict, city: str):
        user_history = UserHistory(
        user_id=user_id,
        city_name=city,
        temperature=data['temperature'],
        feels_like=data['feels_like'],
        humidity=data['humidity'],
        wind=data['wind'],
        weather=data['weather'],
        description=data['description'],
        time=data['time'])
        
        try:
            session.add(user_history)
            session.commit()
            session.refresh(user_history)
        
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


def find_user_history(session: Session, user: dict):
     db_user_history = session.exec(select(UserHistory).where(UserHistory.user_id == user["id"])).all()
     user_history = [history.model_dump() for history in db_user_history]
     return user_history

def find_top_location(session: Session):
         result = session.exec(
                    select(UserHistory.city_name,
                           func.count().label("total")
                           )
                           .group_by(UserHistory.city_name)
                           .order_by(func.count().desc())
                            ).first()
         
         city, total = result

         return{"city_name": city,
                "total": total} 

def find_top_user(session: Session):
    user = session.exec(
        select(UserHistory.user_id,
               func.count().label("total")
               )
               .group_by(UserHistory.user_id)
               .order_by(func.count().desc())
            ).first()
    
    if not user:
          return None
    
    user_id, total = user

    return{
          "user_id": user_id,
          "total": total}