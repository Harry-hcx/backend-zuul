import random

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.room import Room
from app.models.item import Item
from app.models.room_item import RoomItem

ROOM_NAMES = [
    "古书图书馆", "炼金实验室", "兵器库", "机关走廊",
    "监狱牢房", "秘密宝藏室", "最终祭坛",
]

ITEM_POOL = [
    ("火把", 10, 5),
    ("古书（密码书）", 20, 50),
    ("炼金药水（小）", 10, 30),
    ("炼金试剂包", 10, 40),
    ("钥匙", 10, 20),
    ("武器（短剑）", 30, 80),
    ("盾牌", 40, 70),
    ("金币（堆）", 10, 100),
    ("宝石", 10, 200),
    ("魔法饼干", 0, 10),
    ("体力药水", 0, 10),
]

ROOM_COUNT = 100
GRID_WIDTH = 10


async def init_game_data():
    async with async_session() as session:
        count = await session.scalar(select(func.count()).select_from(Room))
        if count and count > 0:
            return

        await session.execute(delete(RoomItem))
        await session.execute(delete(Item))
        await session.execute(delete(Room))
        await session.flush()

        rooms: list[Room] = []
        for i in range(ROOM_COUNT):
            if i == 0:
                name = "入口大厅"
            elif random.random() < 0.1:
                name = "传送房间"
            else:
                name = random.choice(ROOM_NAMES)
            room = Room(room_name=name)
            session.add(room)
            rooms.append(room)

        await session.flush()

        for i, room in enumerate(rooms):
            if room.room_name == "传送房间":
                continue

            row, col = i // GRID_WIDTH, i % GRID_WIDTH
            room.room_up_id = rooms[i - GRID_WIDTH].room_id if row > 0 else None
            room.room_down_id = rooms[i + GRID_WIDTH].room_id if row < GRID_WIDTH - 1 else None
            room.room_left_id = rooms[i - 1].room_id if col > 0 else None
            room.room_right_id = rooms[i + 1].room_id if col < GRID_WIDTH - 1 else None

            item_count = random.randint(2, 10)
            for _ in range(item_count):
                tpl = random.choice(ITEM_POOL)
                item = Item(item_name=tpl[0], item_size=tpl[1], item_value=tpl[2])
                session.add(item)
                await session.flush()
                session.add(RoomItem(room_id=room.room_id, item_id=item.item_id))

        await session.commit()