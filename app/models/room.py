from sqlalchemy import Column, Integer, String

from app.database import Base


class Room(Base):
    __tablename__ = "room"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(100), nullable=False)
    room_up_id = Column(Integer, nullable=True)
    room_down_id = Column(Integer, nullable=True)
    room_left_id = Column(Integer, nullable=True)
    room_right_id = Column(Integer, nullable=True)