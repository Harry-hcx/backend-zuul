from datetime import datetime

from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player
from app.models.backpack import Backpack
from app.models.save_record import SaveRecord
from app.schemas.game import SaveRecordResponse, SaveRecordDetailResponse
from app.schemas.player import LoginResponse
from app.schemas.result import Result


async def list_saves(db: AsyncSession, player_id: int):
    stmt = (
        select(SaveRecord)
        .where(SaveRecord.player_id == player_id)
        .order_by(SaveRecord.save_time.desc())
    )
    records = (await db.execute(stmt)).scalars().all()
    data = [
        SaveRecordResponse(
            save_id=r.save_id,
            player_id=r.player_id,
            save_time=r.save_time,
            player_score=r.player_score,
            player_stamina=r.player_stamina,
            player_room_id=r.player_room_id,
            player_backpack_id=r.player_backpack_id,
        ) for r in records
    ]
    return Result.success(data, "all save records fetched successfully")


async def save_game(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    record = SaveRecord(
        player_id=player_id,
        save_time=datetime.now(),
        player_score=player.player_score,
        player_stamina=player.player_stamina,
        player_room_id=player.player_room_id,
        player_backpack_id=player.player_backpack_id,
    )
    db.add(record)
    await db.commit()
    return Result.success(None, "game saved successfully")


async def read_game(db: AsyncSession, save_id: int):
    record = await db.get(SaveRecord, save_id)
    if not record:
        return Result.error(404, "save record not found")

    player = await db.get(Player, record.player_id)
    if not player:
        return Result.error(404, "player not found for this save record")

    player.player_score = record.player_score
    player.player_stamina = record.player_stamina
    player.player_room_id = record.player_room_id
    player.player_backpack_id = record.player_backpack_id
    await db.commit()

    return Result.success(
        SaveRecordDetailResponse(
            player_id=record.player_id,
            player_name=player.player_name,
            player_score=record.player_score,
            player_stamina=record.player_stamina,
            player_room_id=record.player_room_id,
            player_backpack_id=record.player_backpack_id,
            save_time=record.save_time,
        ),
        "game loaded and player state updated",
    )


async def delete_game(db: AsyncSession, save_id: int):
    record = await db.get(SaveRecord, save_id)
    if not record:
        return Result.error(404, "save record not found")
    await db.delete(record)
    await db.commit()
    return Result.success(None, "game deleted")


async def start_new_game(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    new_backpack = Backpack(player_id=player.player_id, backpack_size=100)
    db.add(new_backpack)
    await db.flush()

    player.player_score = 0
    player.player_stamina = 200
    player.player_backpack_id = new_backpack.backpack_id
    player.player_room_id = 1
    await db.commit()

    return Result.success(LoginResponse(player_id=player.player_id), "new game started")