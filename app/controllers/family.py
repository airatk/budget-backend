from pydantic import BaseModel

from fastapi import APIRouter


family_controller: APIRouter = APIRouter(prefix="/family")


class FamilyData(BaseModel):
    id: int | None


@family_controller.get("/")
async def get_family():
    # TODO: The returned result is data of current user's family.

    pass

@family_controller.post("/create")
async def create_family(family_data: FamilyData):
    # TODO: To create family there should be at least 2 users provided,
    #       and there should be no family with the same members.

    pass

@family_controller.put("/update")
async def update_family(family_data: FamilyData):
    pass

@family_controller.delete("/delete")
async def delete_family(id: int):
    pass
