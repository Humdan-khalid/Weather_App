from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import database_url

DATABASE_URL = database_url

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session