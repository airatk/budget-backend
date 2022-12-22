from pydantic import Field, PositiveInt

from .utilities.base import BaseData


class UserData(BaseData, orm_mode=True):
    id: PositiveInt
    family_id: PositiveInt | None
    username: str = Field(..., min_length=1)
