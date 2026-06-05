import random

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player
from app.models.backpack import Backpack
from app.models.room import Room
from app.schemas.player import (
    LoginResponse, MoveResponse, PlayerListResponse, TransResponse,
)
from app.schemas.result import Result
from app.utils import room_history_store
from app.utils.qiniu_upload import save_avatar


async def login(db: AsyncSession, username: str, password: str):
    stmt = select(Player).where(
        Player.player_name == username,
        Player.player_password == password,
    )
    player = (await db.execute(stmt)).scalar_one_or_none()
    if player:
        return Result.success(LoginResponse(player_id=player.player_id), "login successful")
    return Result.error(401, "invalid username or password")


async def register(db: AsyncSession, player_name: str, password: str, avatar_bytes: bytes | None):
    existing = (await db.execute(
        select(Player).where(Player.player_name == player_name)
    )).scalar_one_or_none()
    if existing:
        return Result.error(409, "player already exists")

    avatar_url = ""
    if avatar_bytes:
        try:
            avatar_url = save_avatar(avatar_bytes, player_name)
        except Exception as e:
            return Result.error(500, f"avatar upload failed: {e}")

    player = Player(
        player_name=player_name,
        player_password=password,
        player_avatar_url=avatar_url,
        player_score=0,
        player_stamina=200,
        player_room_id=1,
    )
    db.add(player)
    await db.flush()

    backpack = Backpack(player_id=player.player_id, backpack_size=100)
    db.add(backpack)
    await db.flush()

    player.player_backpack_id = backpack.backpack_id
    await db.commit()

    return Result.success(LoginResponse(player_id=player.player_id), "register successful")


async def get_player_info(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")
    from app.schemas.player import PlayerInfoResponse
    return Result.success(PlayerInfoResponse(
        player_id=player.player_id,
        player_name=player.player_name,
        player_avatar_url=player.player_avatar_url,
        player_backpack_id=player.player_backpack_id,
        player_score=player.player_score,
        player_room_id=player.player_room_id,
        player_stamina=player.player_stamina,
    ), "success")


async def move_player(db: AsyncSession, player_id: int, direction: str):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    room = await db.get(Room, player.player_room_id)
    if not room:
        return Result.error(404, "current room not found")

    target_map = {
        "up": room.room_up_id,
        "down": room.room_down_id,
        "left": room.room_left_id,
        "right": room.room_right_id,
    }
    target_room_id = target_map.get(direction.lower())
    if not target_room_id:
        return Result.error(400, "no room in that direction")

    target_room = await db.get(Room, target_room_id)
    if not target_room:
        return Result.error(404, "target room not found")

    await room_history_store.push_room_history(db, player_id, player.player_backpack_id or 0, room.room_id)

    player.player_room_id = target_room_id
    player.player_stamina -= 2
    await db.commit()

    return Result.success(MoveResponse(room_id=target_room_id), "success")


async def list_all_players(db: AsyncSession):
    result = await db.execute(select(Player))
    players = result.scalars().all()
    data = [
        PlayerListResponse(
            player_id=p.player_id,
            player_name=p.player_name,
            player_avatar_url=p.player_avatar_url,
            player_score=p.player_score,
        ) for p in players
    ]
    return Result.success(data, "success")


async def teleport_player(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    rooms = (await db.execute(select(Room))).scalars().all()
    if not rooms:
        return Result.error(500, "no available rooms")

    target = random.choice(rooms)
    player.player_room_id = target.room_id
    await db.commit()

    return Result.success(TransResponse(room_id=target.room_id), "teleport successful")


async def back_player(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    if not await room_history_store.has_room_history(db, player_id, player.player_backpack_id or 0):
        return Result.error(404, "previous room not found")

    previous_room_id = await room_history_store.pop_room_history(db, player_id, player.player_backpack_id or 0)

    player.player_room_id = previous_room_id
    player.player_stamina -= 2
    await db.commit()

    return Result.success(TransResponse(room_id=previous_room_id), "success")


async def home_player(db: AsyncSession, player_id: int):
    player = await db.get(Player, player_id)
    if not player:
        return Result.error(404, "player not found")

    await room_history_store.push_room_history(db, player_id, player.player_backpack_id or 0, player.player_room_id)

    player.player_room_id = 1
    player.player_stamina -= 2
    await db.commit()

    return Result.success(None, "回城成功")


async def update_score(db: AsyncSession, player_id: int):
    await db.execute(text("""
        UPDATE player SET player_score = (
            SELECT IFNULL(SUM(i.item_value), 0)
            FROM backpack_item bi JOIN item i ON bi.item_id = i.item_id
            WHERE bi.backpack_id = player.player_backpack_id
        ) WHERE player_id = :pid
    """), {"pid": player_id})
    await db.commit()