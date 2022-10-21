from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


family_controller: APIRouter = APIRouter(prefix="/family")


class FamilyData(BaseModel):
    id: int | None

    class Config:
        orm_mode = True


@family_controller.get("/", response_model=FamilyData)
async def get_family(current_user: User = Depends(identify_user)):
    # TODO: The returned result is data of current user's family.

    pass

@family_controller.post("/create", response_model=str)
async def create_family(family_data: FamilyData, current_user: User = Depends(identify_user)):
    # TODO: To create family there should be at least 2 users provided,
    #       and there should be no family with the same members.

    pass

@family_controller.put("/update", response_model=str)
async def update_family(family_data: FamilyData, current_user: User = Depends(identify_user)):
    pass

@family_controller.delete("/delete", response_model=str)
async def delete_family(id: int, current_user: User = Depends(identify_user)):
    pass
