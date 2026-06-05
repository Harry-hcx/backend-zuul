from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.backpack import BackpackListRequest, BackpackItemActionRequest
from app.services import backpack_service

router = APIRouter()


@router.post("/list")
async def get_backpack(req: BackpackListRequest, db: AsyncSession = Depends(get_db)):
    return await backpack_service.get_backpack_by_player_id(db, req.player_id)


@router.post("/pick")
async def pick_item(req: BackpackItemActionRequest, db: AsyncSession = Depends(get_db)):
    return await backpack_service.pick_item(db, req.player_id, req.item_id)


@router.post("/throw")
async def throw_item(req: BackpackItemActionRequest, db: AsyncSession = Depends(get_db)):
    return await backpack_service.throw_item(db, req.player_id, req.item_id)


@router.post("/use")
async def use_item(req: BackpackItemActionRequest, db: AsyncSession = Depends(get_db)):
    return await backpack_service.use_item(db, req.player_id, req.item_id)