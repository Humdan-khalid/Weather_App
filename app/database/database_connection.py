from sqlmodel import create_engine, Session
from app.core.config import database_url
from app.core.exceptions import DatabaseUrlNotFound

def valid_database_config():
    if not database_url:
        raise DatabaseUrlNotFound("Database_url not found!")


def get_engine():
    valid_database_config()
    return create_engine(
        database_url,
        echo=False,
        max_overflow=10,
        pool_size=5
)

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session