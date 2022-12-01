from pydantic import BaseModel, PositiveInt

from .utilities.types import NonEmptyStr


class UserData(BaseModel, orm_mode=True):
    id: PositiveInt
    family_id: PositiveInt | None
    username: NonEmptyStr
