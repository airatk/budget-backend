from pydantic import Field

from .user import UserData
from .utilities.base import BaseData


class FamilyOutputData(BaseData, orm_mode=True):
    access_code: str = Field(..., min_length=1)

    members: list[UserData] = Field(..., min_items=1)

class FamilyInputData(BaseData, anystr_strip_whitespace=True):
    access_code: str = Field(..., min_length=1)
