from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.room import RoomInfoRequest
from app.services import room_service

router = APIRouter()


@router.post("/info")
async def get_room_info(req: RoomInfoRequest, db: AsyncSession = Depends(get_db)):
    return await room_service.get_room_info(db, req.room_id)