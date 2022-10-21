from pydantic import BaseModel

from .user import UserData


class FamilyData(BaseModel):
    access_code: str
    members: list[UserData] | None

    class Config:
        orm_mode = True
