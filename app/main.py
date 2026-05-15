from fastapi import FastAPI, Request
from app.core.middleware import log_request_middleware
from app.core.exceptions import DatabaseUrlNotFound, TokenExpired, SecretDataNotFound
from fastapi.responses import JSONResponse
from app.api import users, weather, history, admins

app = FastAPI()

app.middleware("http")(log_request_middleware)

@app.exception_handler(DatabaseUrlNotFound)
def database_url_exception(request: Request, exc: DatabaseUrlNotFound):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

@app.exception_handler(TokenExpired)
def token_expired(request: Request, exc: TokenExpired):
    return JSONResponse(
        status_code= 401,
        content={"detail": "Token has expired!"}
    )

@app.exception_handler(SecretDataNotFound)
def token_expired(request: Request, exc: SecretDataNotFound):
    return JSONResponse(
        status_code= 500,
        content={"detail": str(exc)}
    )

app.include_router(users.router)

app.include_router(weather.router)

app.include_router(history.router)

app.include_router(admins.router)