from sqlalchemy import select, delete as sa_delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.room_history import RoomHistory


async def push_room_history(db: AsyncSession, player_id: int, backpack_id: int, room_id: int) -> None:
    db.add(RoomHistory(player_id=player_id, backpack_id=backpack_id, room_id=room_id))
    await db.flush()


async def pop_room_history(db: AsyncSession, player_id: int, backpack_id: int) -> int | None:
    stmt = (
        select(RoomHistory)
        .where(RoomHistory.player_id == player_id, RoomHistory.backpack_id == backpack_id)
        .order_by(RoomHistory.id.desc())
        .limit(1)
    )
    record = (await db.execute(stmt)).scalar_one_or_none()
    if record is None:
        return None
    await db.execute(
        sa_delete(RoomHistory).where(RoomHistory.id == record.id)
    )
    return record.room_id


async def has_room_history(db: AsyncSession, player_id: int, backpack_id: int) -> bool:
    stmt = select(func.count()).where(
        RoomHistory.player_id == player_id,
        RoomHistory.backpack_id == backpack_id,
    )
    count = (await db.execute(stmt)).scalar()
    return (count or 0) > 0