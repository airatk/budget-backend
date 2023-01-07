from pydantic import Field, PositiveInt

from app.utilities.constants import MIN_PASSWORD_LENGTH

from .utilities.base import BaseData


class UserOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    family_id: PositiveInt | None
    username: str

class UserCreationData(BaseData, anystr_strip_whitespace=True):
    family_id: PositiveInt | None
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH)
