from sqlalchemy import Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100), nullable=False)
    item_size = Column(Integer, nullable=False, default=0)
    item_value = Column(Integer, default=0)