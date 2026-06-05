from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ListRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int


class SaveRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int


class ReadRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    save_id: int


class DeleteRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    save_id: int


class StartGameRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int


class SaveRecordResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    save_id: int
    player_id: int
    save_time: Optional[datetime] = None
    player_score: Optional[int] = None
    player_stamina: Optional[int] = None
    player_room_id: Optional[int] = None
    player_backpack_id: Optional[int] = None


class SaveRecordDetailResponse(BaseModel):
    """用于 /game/read 返回，包含玩家名称"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int
    player_name: str
    player_score: Optional[int] = None
    player_stamina: Optional[int] = None
    player_room_id: Optional[int] = None
    player_backpack_id: Optional[int] = None
    save_time: Optional[datetime] = None