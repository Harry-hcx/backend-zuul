from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player
from app.models.backpack import Backpack, BackpackItem
from app.models.item import Item
from app.models.room_item import RoomItem
from app.schemas.backpack import BackpackResponse, ItemDTO
from app.schemas.result import Result
from app.services.player_service import update_score


async def get_backpack_by_player_id(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")
    if not player.player_backpack_id:
        return Result.error(404, "player has no backpack")

    backpack = await db.get(Backpack, player.player_backpack_id)
    if not backpack:
        return Result.error(404, "backpack not found")

    relations = (await db.execute(
        select(BackpackItem).where(BackpackItem.backpack_id == backpack.backpack_id)
    )).scalars().all()

    item_ids = [r.item_id for r in relations]
    items = []
    if item_ids:
        items = (await db.execute(select(Item).where(Item.item_id.in_(item_ids)))).scalars().all()

    item_dtos = [
        ItemDTO(item_id=i.item_id, item_name=i.item_name, item_size=i.item_size, item_value=i.item_value)
        for i in items
    ]

    return Result.success(
        BackpackResponse(backpack_id=backpack.backpack_id, backpack_size=backpack.backpack_size, item_list=item_dtos),
        "success",
    )


async def pick_item(db: AsyncSession, player_id: int, item_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")
    if not player.player_backpack_id:
        return Result.error(404, "player has no backpack")
    if not player.player_room_id:
        return Result.error(400, "player is not in a valid room")

    item = await db.get(Item, item_id)
    if not item:
        return Result.error(404, "item not found")

    room_item = (await db.execute(
        select(RoomItem).where(RoomItem.room_id == player.player_room_id, RoomItem.item_id == item_id)
    )).scalar_one_or_none()
    if not room_item:
        return Result.error(404, "item not found in current room")

    existing = (await db.execute(
        select(BackpackItem).where(
            BackpackItem.backpack_id == player.player_backpack_id,
            BackpackItem.item_id == item_id,
        )
    )).scalar_one_or_none()
    if existing:
        return Result.error(409, "item already in backpack")

    db.add(BackpackItem(backpack_id=player.player_backpack_id, item_id=item_id))
    await db.execute(
        sa_delete(RoomItem).where(RoomItem.room_id == player.player_room_id, RoomItem.item_id == item_id)
    )

    player.player_stamina -= 2
    await db.commit()
    await update_score(db, player_id)

    return Result.success(None, "item picked successfully")


async def throw_item(db: AsyncSession, player_id: int, item_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")
    if not player.player_backpack_id:
        return Result.error(404, "player has no backpack")
    if not player.player_room_id:
        return Result.error(400, "player is not in a valid room")

    result = await db.execute(
        sa_delete(BackpackItem).where(
            BackpackItem.backpack_id == player.player_backpack_id,
            BackpackItem.item_id == item_id,
        )
    )
    if result.rowcount == 0:
        return Result.error(404, "item not found in backpack")

    db.add(RoomItem(room_id=player.player_room_id, item_id=item_id))
    player.player_stamina -= 2
    await db.commit()
    await update_score(db, player_id)

    return Result.success(None, "item dropped to room successfully")


async def use_item(db: AsyncSession, player_id: int, item_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")
    if not player.player_backpack_id:
        return Result.error(404, "player has no backpack")

    item = await db.get(Item, item_id)
    if not item:
        return Result.error(404, "item not found")

    item_name = item.item_name

    result = await db.execute(
        sa_delete(BackpackItem).where(
            BackpackItem.backpack_id == player.player_backpack_id,
            BackpackItem.item_id == item_id,
        )
    )
    if result.rowcount == 0:
        return Result.error(404, "item not found in backpack or already used")

    await db.delete(item)

    if item_name == "魔法饼干":
        backpack = await db.get(Backpack, player.player_backpack_id)
        if backpack:
            backpack.backpack_size += 10
    elif item_name == "体力药水":
        player.player_stamina += 10
    else:
        player.player_stamina -= 2

    await db.commit()
    await update_score(db, player_id)

    return Result.success(None, "item used and removed successfully")