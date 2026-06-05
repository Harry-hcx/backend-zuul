from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from app.database import Base


class SaveRecord(Base):
    __tablename__ = "save_record"

    save_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, nullable=False)
    save_time = Column(DateTime, nullable=False, default=datetime.now)
    player_score = Column(Integer, nullable=True)
    player_stamina = Column(Integer, nullable=True)
    player_room_id = Column(Integer, nullable=True)
    player_backpack_id = Column(Integer, nullable=True)