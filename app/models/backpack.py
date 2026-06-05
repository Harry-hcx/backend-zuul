from sqlalchemy import Column, Integer

from app.database import Base


class Backpack(Base):
    __tablename__ = "backpack"

    backpack_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, nullable=False)
    backpack_size = Column(Integer, nullable=False, default=100)


class BackpackItem(Base):
    __tablename__ = "backpack_item"

    backpack_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, primary_key=True)