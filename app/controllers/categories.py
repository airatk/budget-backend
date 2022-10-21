from sqlalchemy.orm import Session

from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.models import User
from app.models import Category
from app.models.category import CategoryType


categories_controller: APIRouter = APIRouter(prefix="/categories")


class CategoryData(BaseModel):
    id: int | None
    base_category_id: int | None
    name: str
    type: CategoryType

    class Config:
        orm_mode = True


@categories_controller.get("/list", response_model=list[CategoryData])
async def get_categories(current_user: User = Depends(identify_user)):
    return [ CategoryData.from_orm(obj=category) for category in current_user.categories ]

@categories_controller.get("/item", response_model=CategoryData)
async def get_category(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    category: Category = session.query(Category).\
        filter(
            Category.id == id, 
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No category with given `id` was found")

    return CategoryData.from_orm(obj=category)

@categories_controller.post("/create", response_model=str)
async def create_category(category_data: CategoryData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    category: Category = Category(
        user=current_user,
        base_category_id=category_data.base_category_id,
        name=category_data.name,
        type=category_data.type
    )

    session.add(category)
    session.commit()

    return "Category was created"

@categories_controller.put("/update", response_model=str)
async def update_category(category_data: CategoryData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    category: Category | None = session.query(Category).\
        filter(
            Category.id == category_data.id,
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No category with given `id` was found")

    category.base_category_id = category_data.base_category_id
    category.name = category_data.name
    category.type = category_data.type

    session.commit()

    return "Category was updated"

@categories_controller.delete("/delete", response_model=str)
async def delete_category(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    category: Category | None = session.query(Category).\
        filter(
            Category.id == id,
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No category with given `id` was found")

    session.delete(category)
    session.commit()

    return "Category was deleted"
