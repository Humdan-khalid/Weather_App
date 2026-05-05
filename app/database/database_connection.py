from sqlmodel import create_engine, Session
from app.core.config import database_url
from app.core.exceptions import DatabaseUrlNotFound
from app.core.log_config import logger

def valid_database_config():
    if not database_url:
        logger.error(f"database_url is missing!")   
        raise DatabaseUrlNotFound("Database_url not found!")
    
valid_database_config()


engine = create_engine(
    database_url,
    echo=False,
    max_overflow=10,
    pool_size=5
)

def get_session():
    with Session(engine) as session:
        yield session