from sqlalchemy import Column, Integer

from app.database import Base


class RoomItem(Base):
    __tablename__ = "room_item"

    room_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, primary_key=True)