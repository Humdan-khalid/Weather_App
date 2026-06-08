import sys
import asyncio
import pytest
import pytest_asyncio
from app.database.test_database_connection import AsyncSessionLocal

# Windows par asyncpg ke issues prevent karne ke liye policy set karna
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Database session fixture
@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Teardown ko safely handle karne ke liye pehle rollback then close
            await session.rollback()
            await session.close()