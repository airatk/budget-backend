from .user import UserData
from .utilities.base import BaseData
from .utilities.types import NonEmptyStr


class FamilyOutputData(BaseData, orm_mode=True):
    access_code: NonEmptyStr
    members: list[UserData]

class FamilyInputData(BaseData, anystr_strip_whitespace=True):
    access_code: NonEmptyStr
