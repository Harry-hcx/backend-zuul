from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.player import (
    LoginRequest, PlayerInfoRequest, MoveRequest, TransRequest,
)
from app.services import player_service

router = APIRouter()


@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.login(db, req.username, req.password)


@router.post("/register")
async def register(
    playerName: str = Form(...),
    password: str = Form(...),
    avatar: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    avatar_bytes = await avatar.read() if avatar else None
    return await player_service.register(db, playerName, password, avatar_bytes)


@router.post("/info")
async def get_info(req: PlayerInfoRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.get_player_info(db, req.player_id)


@router.post("/move")
async def move(req: MoveRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.move_player(db, req.player_id, req.direction)


@router.get("/list")
async def list_players(db: AsyncSession = Depends(get_db)):
    return await player_service.list_all_players(db)


@router.post("/trans")
async def teleport(req: TransRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.teleport_player(db, req.player_id)


@router.post("/back")
async def back(req: TransRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.back_player(db, req.player_id)


@router.post("/home")
async def home(req: TransRequest, db: AsyncSession = Depends(get_db)):
    return await player_service.home_player(db, req.player_id)