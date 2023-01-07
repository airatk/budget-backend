from pydantic import Field

from .user import UserOutputData
from .utilities.base import BaseData


class FamilyOutputData(BaseData, orm_mode=True):
    access_code: str

    members: list[UserOutputData]

class FamilyInputData(BaseData, anystr_strip_whitespace=True):
    access_code: str = Field(..., min_length=1)
