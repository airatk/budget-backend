from pydantic import PositiveInt

from .utilities.base import BaseData
from .utilities.types import NonEmptyStr


class UserData(BaseData, orm_mode=True):
    id: PositiveInt
    family_id: PositiveInt | None
    username: NonEmptyStr
