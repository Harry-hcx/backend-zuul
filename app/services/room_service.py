from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.room import Room
from app.models.item import Item
from app.models.room_item import RoomItem
from app.schemas.room import RoomInfoResponse, ItemDTO
from app.schemas.result import Result


async def get_room_info(db: AsyncSession, room_id: int):
    room = await db.get(Room, room_id)
    if not room:
        return Result.error(404, "room not found")

    stmt = select(RoomItem).where(RoomItem.room_id == room_id)
    relations = (await db.execute(stmt)).scalars().all()

    if not relations:
        return Result.success(
            RoomInfoResponse(room_id=room.room_id, room_name=room.room_name, items=[]),
            "no items in room",
        )

    item_ids = [r.item_id for r in relations]
    items = (await db.execute(select(Item).where(Item.item_id.in_(item_ids)))).scalars().all()

    item_dtos = [
        ItemDTO(item_id=i.item_id, item_name=i.item_name, item_size=i.item_size, item_value=i.item_value)
        for i in items
    ]

    return Result.success(
        RoomInfoResponse(room_id=room.room_id, room_name=room.room_name, items=item_dtos),
        "success",
    )