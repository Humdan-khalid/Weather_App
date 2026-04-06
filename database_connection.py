from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from database import SQLModel
import os
from log_config import logger

load_dotenv()


database_url=os.getenv("DATABASE_URL")

if not database_url:
    logger.critical("Database url not found")
    raise ValueError("database_url not found!")

engine = create_engine(
    database_url,
    echo=False,
    max_overflow=10,
    pool_size=5
)

def create_tables():
    SQLModel.metadata.create_all(engine)

create_tables()

def get_session():
    with Session(engine) as session:
        yield session