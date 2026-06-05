from sqlalchemy import Column, Integer

from app.database import Base


class RoomHistory(Base):
    __tablename__ = "room_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, nullable=False, index=True)
    backpack_id = Column(Integer, nullable=False)
    room_id = Column(Integer, nullable=False)