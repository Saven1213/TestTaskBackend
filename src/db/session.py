from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from src.config import settings
from .models.base import Base


engine: AsyncEngine = create_async_engine(
    url=settings.db_url_asyncpg()
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

