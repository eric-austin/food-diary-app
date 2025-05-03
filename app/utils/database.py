from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.utils.config import settings # Use your actual config path

DATABASE_URL = str(settings.DATABASE_URL) # Ensure it's a string

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=(settings.APP_ENV == 'development'), # Log SQL in dev
    pool_pre_ping=True,
)

# Create a configured "Session" class
# expire_on_commit=False prevents attributes from expiring after commit
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get a DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit() # Commit transaction if no exceptions
        except Exception:
            await session.rollback() # Rollback on error
            raise
        finally:
            await session.close() # Close session

# Context manager version (alternative way to use session)
@asynccontextmanager
async def db_session_manager() -> AsyncGenerator[AsyncSession, None]:
     async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def close_db():
    await engine.dispose()