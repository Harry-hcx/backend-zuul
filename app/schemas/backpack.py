from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BackpackListRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int


class BackpackItemActionRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    player_id: int
    item_id: int


class ItemDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    item_id: int
    item_name: str
    item_size: int
    item_value: int


class BackpackResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    backpack_id: int
    backpack_size: int
    item_list: list[ItemDTO] = []