from fastapi import FastAPI, status, HTTPException, Depends, Header
import httpx
from sqlmodel import Session, select, func
from database import Users , CreateUsers, UsersLogin, UserHistory, ReadUser, LoginModel, Admins, CreateAdmin, ReadAdmin, LoginAdmin
from password_hash import create_hash_password, verify_hash_password
from database_connection import engine, get_session
from jwt import create_token, user_token
from datetime import datetime
import os
import asyncio
from caching import r
import json
from log_config import logger

weather_api_key = os.getenv("WEATHER_API_KEY")
app_url = os.getenv("URL")

if not weather_api_key:
    logger.critical("Weather API key not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="weather api key not found!")

if not app_url:
    logger.critical("App Url not found!")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App URL not found!")

app = FastAPI()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def create_user(user: CreateUsers, session: Session = Depends(get_session)):
    db_user = session.exec(select(Users).where(Users.email == user.email)).first()
    
    if db_user:
        logger.warning("Account already created with this email: %s", user.email)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="account already exist with email")

    new_user = Users(
        name=user.name.title(),
        age=user.age,
        phone_number=user.phone_number,
        email=user.email.lower(),
        password=create_hash_password(user.password)
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except Exception as e:
        session.rollback()
        logger.critical("Database Problem", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Problem!")

    logger.info("User account created successfully with this email: %s", user.email)
    return new_user

@app.post("/login/users", status_code=status.HTTP_200_OK, response_model=LoginModel)
def login_users(user: UsersLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(Users).where(Users.email == user.email.lower())).first()

    if not db_user:
        logger.warning("Invalid login attempt with email %s", user.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    

    verify_password = verify_hash_password(user.password , db_user.password)
    
    if not verify_password:
        logger.warning("Invalid login attempt with wrong password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
    token = create_token(
        {
        "id": db_user.id,
        "email": db_user.email
        }
    )

    logger.info("User login successfully with this email %s", user.email)
    return{"access_token": token,
           "token_type": "Bearer"}

@app.get("/weather", status_code=status.HTTP_200_OK)
async def get_weather(city_name: str, session: Session=Depends(get_session), user: dict = Depends(user_token)):

    db_user = session.exec(select(Users).where(Users.id == user["id"])).first()

    if not db_user:
        logger.warning("User attempt failed with wrong token %s", user["email"])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!")
    
    city = city_name.title()

    cache = f"name: {city}"
    cached = r.hgetall(cache)

    current_time = {"time": datetime.now().strftime("%H:%M:%S")}
    
    if cached:
        user_history = UserHistory(
        user_id=user["id"],
        name=db_user.name,
        city_name=city,
        temperature=cached["temperature"],
        feels_like=cached['feels_like'],
        humidity=cached['humidity'],
        wind=cached['wind'],
        weather=cached['weather'],
        description=cached['description'],
        time=current_time["time"])

        try:
            session.add(user_history)
            session.commit()
        
        except Exception as e:
            session.rollback()
            logger.critical("Database error", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error!")
        
        logger.info("Weather data come to the cache.")
        return cached

    url = app_url

    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()  

    if response.status_code != 200:
        logger.info("City not found! %s", city)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found!")
    

    user_history = UserHistory(
        user_id=user["id"],
        name=db_user.name,
        city_name=city,
        temperature=data["main"]["temp"],
        feels_like=data['main']['feels_like'],
        humidity=data['main']['humidity'],
        wind=data['wind']['speed'],
        weather=data['weather'][0]['main'],
        description=data['weather'][0]['description'],
        time=current_time["time"]
    )

    result = {
        "temperature": data['main']['temp'],
        "feels_like": data['main']['feels_like'],
        "humidity": data['main']['humidity'],
        "wind": data['wind']['speed'],
        "weather": data['weather'][0]['main'],
        "description": data['weather'][0]['description'],
        "time": current_time["time"]
        }
    
    r.hset(cache, mapping=result)
    r.expire(cache, 300)

    try:
        session.add(user_history)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.critical("Databse error!", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error!")

    logger.info("Weather data come to the Api key.")
    return result

@app.get("/get_user_history", status_code=status.HTTP_200_OK)
def get_user_history(session: Session = Depends(get_session), user: dict = Depends(user_token)):
    db_user = session.exec(select(Users).where(Users.email == user["email"])).first()

    if not db_user:
        logger.warning("Invalid user try to get the user history with this email %s", user["email"])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user try to get the user history")
    
    cache_key = f"user_id:{user['id']}"
    cached = r.get(cache_key)

    if cached:
        logger.info("Weather data come to the cache")
        return {"Weather_History": json.loads(cached)}
    
    db_user_history = session.exec(select(UserHistory).where(UserHistory.user_id == user["id"])).all()

    if not db_user_history:
        logger.warning("User History are not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User History are not found!")

    
    data = [history.dict() for history in db_user_history]
        

    r.set(cache_key, json.dumps(data), ex=50)

    logger.info("Weather data come to the database.")
    return{"Weather_History": db_user_history}


@app.get("/searching", status_code=status.HTTP_200_OK)
def get_top_search_city(session: Session = Depends(get_session), admin: dict = (user_token)):
    db_admin = session.exec(
        select(
            Admins.email == admin['email']
        )
    ).first()

    if not db_admin:
        logger.warning("Admin not found!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found!")

    find_city = session.exec(
                    select(UserHistory.city_name,
                           func.count().label("total")
                           )
                           .group_by(UserHistory.city_name)
                           .order_by(func.count().desc())
                            ).first()
    
    if not find_city:
        logger.warning("City not found!", exc_info=True)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found!")

    return {"City": find_city.city_name,
            "total searches": find_city.total}

@app.get("/user", status_code=status.HTTP_200_OK)
def get_top_user(session: Session = Depends(get_session), admin: dict = Depends(user_token)):
    db_admin = session.exec(
                select(Admins).where(Admins.email == admin["email"])
                ).first()
    
    if not db_admin:
        logger.warning("admin failed login attempt with email %s", admin['email'])
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found!")
    
    db_user = session.exec(
        select(UserHistory.user_id, UserHistory.name,
               func.count().label("total")
               )
               .group_by(UserHistory.user_id, UserHistory.name)
               .order_by(func.count().desc())
            ).first()
    
    if not db_user:
        logger.warning("top user not found in database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Top user not found!")
    
    return{
            "user_name": db_user.name,
            "user_id": db_user.user_id,
            "total searches": db_user.total
           }


@app.post("/admin", status_code=status.HTTP_201_CREATED,response_model=ReadAdmin)
def create_admin(create_admin: CreateAdmin, session: Session=Depends(get_session)):
    db_admin = session.exec(
        select(Admins).where(Admins.email == create_admin.email)
    ).first()

    if db_admin:
        logger.warning("account already exist with this email %s ", create_admin.email)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="account already exist with email.")
    
    new_admin = Admins(
        name=create_admin.name,
        age=create_admin.age,
        phone_number=create_admin.phone_number,
        email=create_admin.email,
        password=create_hash_password(create_admin.password)        
    )

    try:
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)
    
    except Exception as e:
        session.rollback()
        logger.critical("Database error!", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")
        
    logger.info("new admin created successfully with this email %s ", new_admin.email)
    return new_admin

@app.post("/login/admins", status_code=status.HTTP_200_OK)
def admin_login(admin: LoginAdmin, session: Session = Depends(get_session)):
    db_admin = session.exec(
        select(Admins).where(Admins.email == admin.email)
    ).first()

    if not db_admin:
        logger.warning("Invalid login attempt with this email %s ", admin.email)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password!.")
    
    user_password = verify_hash_password(admin.password, db_admin.password)

    if user_password:
        token = create_token(
            {
            "id": db_admin.id,
            "email": db_admin.email}
        )

        logger.info("Admin loggin successfully with this email %s ", admin.email)
        return {"access_token": token,
                "token_type": "Bearer"}
