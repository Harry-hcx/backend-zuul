from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.game import ListRequest, SaveRequest, ReadRequest, DeleteRequest, StartGameRequest
from app.services import game_service

router = APIRouter()


@router.post("/list")
async def list_saves(req: ListRequest, db: AsyncSession = Depends(get_db)):
    return await game_service.list_saves(db, req.player_id)


@router.post("/save")
async def save(req: SaveRequest, db: AsyncSession = Depends(get_db)):
    return await game_service.save_game(db, req.player_id)


@router.post("/read")
async def read(req: ReadRequest, db: AsyncSession = Depends(get_db)):
    return await game_service.read_game(db, req.save_id)


@router.post("/delete")
async def delete(req: DeleteRequest, db: AsyncSession = Depends(get_db)):
    return await game_service.delete_game(db, req.save_id)


@router.post("/new")
async def new_game(req: StartGameRequest, db: AsyncSession = Depends(get_db)):
    return await game_service.start_new_game(db, req.player_id)