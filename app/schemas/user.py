from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    family_id: int | None
    username: str

    class Config:
        orm_mode = True
