from pydantic import BaseModel
from pydantic import PositiveInt

from .utilities.types import NonEmptyStr


class UserData(BaseModel, orm_mode=True):
    id: PositiveInt
    family_id: PositiveInt | None
    username: NonEmptyStr
