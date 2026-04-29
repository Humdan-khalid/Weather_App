from fastapi import Request
import time
from app.utils.log_config import logger

async def log_request_middleware(request: Request, call_next):
    start_time = time.time()

    method = request.method
    url = request.url.path

    response = await call_next(request)

    end_time = time.time()
    duration = end_time - start_time    

    logger.info(f"{method} {url} - {duration:.4f}s")

    return response
