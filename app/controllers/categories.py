from pydantic import BaseModel

from fastapi import APIRouter


categories_controller: APIRouter = APIRouter(prefix="/categories")


class CategoryData(BaseModel):
    id: int | None


@categories_controller.get("/list")
async def get_categories():
    pass

@categories_controller.get("/item")
async def get_category(id: int):
    pass

@categories_controller.post("/create")
async def create_category(category_data: CategoryData):
    pass

@categories_controller.put("/update")
async def update_category(category_data: CategoryData):
    pass

@categories_controller.delete("/delete")
async def delete_category(id: int):
    pass
