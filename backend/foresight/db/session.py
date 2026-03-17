from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from foresight.config import DB_URL, ensure_data_dir
from foresight.db.models import Base

engine = None
SessionLocal = None


async def init_db():
    global engine, SessionLocal
    ensure_data_dir()
    engine = create_async_engine(DB_URL, echo=False)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
