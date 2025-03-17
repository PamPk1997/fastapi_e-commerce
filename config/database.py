from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Use an async database URL (e.g., asyncpg for PostgreSQL)
DATABASE_URL = f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker for AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency for getting the database session
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
