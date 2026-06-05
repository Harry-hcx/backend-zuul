from sqlalchemy import Column, Integer, String

from app.database import Base


class Player(Base):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String(100), nullable=False)
    player_password = Column(String(100), nullable=False)
    player_avatar_url = Column(String(255), nullable=True)
    player_score = Column(Integer, default=0)
    player_stamina = Column(Integer, default=200)
    player_backpack_id = Column(Integer, nullable=True)
    player_room_id = Column(Integer, nullable=True)