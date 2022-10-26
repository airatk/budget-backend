from pydantic import BaseModel
from pydantic import PositiveInt


class UserData(BaseModel):
    id: PositiveInt
    family_id: PositiveInt | None
    username: str

    class Config:
        orm_mode = True
