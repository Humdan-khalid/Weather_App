import json
import redis.asyncio as redis
from app.core.log_config import logger

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


async def get_weather_data_from_cache(city_name: str):

    city = city_name.title()

    data = f"weather:{city}"
    cached = await r.hgetall(data)

    if not cached:
        return None
    
    logger.info(f"{city} weather data came from the cache.")
    return {
        k: v for k, v in cached.items()
        }


async def set_cached(city: str, data: dict):
    key=f"weather:{city}"
    await r.hset(key, mapping=data)
    await r.expire(key, 300)


async def get_user_weather_history_from_cache(user_id: int):
    cache_key = f"user:{user_id}"
    cached = await r.get(cache_key)

    if not cached:
        return None
    
    
    return cached

async def save_history_in_cache(data: dict, user: dict):
    key = f"user:{user['id']}"
    await r.set(key, json.dumps(data))
    await r.expire(key, 300)
