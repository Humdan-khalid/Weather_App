from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os
from app.utils.log_config import logger

load_dotenv()

database_url=os.getenv("DATABASE_URL")

if not database_url:
    logger.critical("Database url not found!")
    raise ValueError("Internal server error")

engine = create_engine(
    database_url,
    echo=False,
    max_overflow=10,
    pool_size=5
)

def get_session():
    with Session(engine) as session:
        yield session