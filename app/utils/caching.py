from app.database_models.user_data_history import UserHistory
from app.repository.auth_repo import user_authentication_with_email
from datetime import datetime
import json
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def get_weather_data_from_cache(city_name: str):

    city = city_name.title()

    data = f"weather:{city}"
    cached = r.hgetall(data)

    if not cached:
        return None
     
    return {
        k: v for k, v in cached.items()
        }


def set_cached(city: str, data: dict):
    key=f"weather:{city}"
    r.hset(key, mapping=data)
    r.expire(key, 300)


def get_history_from_cache(user_id: int):
    cache_key = f"user:{user_id}"
    cached = r.get(cache_key)

    return cached

def save_history_in_cache(data: dict, user: dict):
    key = f"user:{user['id']}"
    r.set(key, json.dumps(data))
    r.expire(key, 300)
