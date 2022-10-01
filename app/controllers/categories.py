from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


categories_controller: APIRouter = APIRouter(prefix="/categories")


class CategoryData(BaseModel):
    id: int | None


@categories_controller.get("/list")
async def get_categories(current_user: User = Depends(identify_user)):
    pass

@categories_controller.get("/item")
async def get_category(id: int, current_user: User = Depends(identify_user)):
    pass

@categories_controller.post("/create")
async def create_category(category_data: CategoryData, current_user: User = Depends(identify_user)):
    pass

@categories_controller.put("/update")
async def update_category(category_data: CategoryData, current_user: User = Depends(identify_user)):
    pass

@categories_controller.delete("/delete")
async def delete_category(id: int, current_user: User = Depends(identify_user)):
    pass
