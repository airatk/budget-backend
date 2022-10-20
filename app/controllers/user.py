from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


user_controller: APIRouter = APIRouter(prefix="/user")


class CurrentUser(BaseModel):
    id: int
    family_id: int | None
    username: str

    class Config:
        orm_mode = True


@user_controller.get("/current", response_model=CurrentUser)
async def get_current_user(current_user: User = Depends(identify_user)):
    return CurrentUser.from_orm(obj=current_user)
