from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    from app.models import Player, Room, Item, Backpack, BackpackItem, RoomItem, SaveRecord, RoomHistory  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # 补齐历史数据库中可能缺失的列（SQLite 的 create_all 不会给已存在的表加列）
        for sql in [
            "ALTER TABLE player ADD COLUMN player_bonus_score INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE save_record ADD COLUMN player_bonus_score INTEGER DEFAULT 0",
        ]:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass  # 列已存在时忽略


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session