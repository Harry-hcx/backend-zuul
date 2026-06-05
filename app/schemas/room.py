from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RoomInfoRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: Optional[int] = None
    room_id: int


class ItemDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    item_id: int
    item_name: str
    item_size: int
    item_value: int


class RoomInfoResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    room_id: int
    room_name: str
    items: list[ItemDTO] = []