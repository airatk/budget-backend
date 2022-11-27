from pydantic import BaseModel

from .utilities.types import NonEmptyStr
from .user import UserData


class FamilyOutputData(BaseModel, orm_mode=True):
    access_code: NonEmptyStr
    members: list[UserData]

class FamilyInputData(BaseModel, anystr_strip_whitespace=True):
    access_code: NonEmptyStr
