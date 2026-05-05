import json
import redis
from app.core.log_config import logger

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
    
    logger.info(f"{city} weather data came from the cache.")
    return {
        k: v for k, v in cached.items()
        }


def set_cached(city: str, data: dict):
    key=f"weather:{city}"
    r.hset(key, mapping=data)
    r.expire(key, 300)


def get_user_weather_history_from_cache(user_id: int):
    cache_key = f"user:{user_id}"
    cached = r.get(cache_key)

    if not cached:
        return None
    
    
    return cached

def save_history_in_cache(data: dict, user: dict):
    key = f"user:{user['id']}"
    r.set(key, json.dumps(data))
    r.expire(key, 300)
