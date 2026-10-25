from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from app.core.config import get_settings, Settings
from typing import Annotated, TypeAlias, AsyncIterator
from fastapi import Depends
settings: Settings = get_settings()

engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG, # logs sql queries
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"server_settings": {"search_path": settings.DB_SCHEMA}}
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_ = AsyncSession,
    expire_on_commit = False,
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

SessionDep: TypeAlias = Annotated[AsyncSession, Depends(dependency=get_session, scope="function")]

StreamingSessionDep: TypeAlias = Annotated[AsyncSession, Depends(dependency=get_session)]