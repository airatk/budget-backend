from sqlalchemy.orm import Session

from pydantic import PositiveInt

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from models import User
from models import Category

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user

from app.schemas.category import CategoryOutputData
from app.schemas.category import CategoryCreationData
from app.schemas.category import CategoryUpdateData


categories_controller: APIRouter = APIRouter(prefix="/categories")


@categories_controller.get("/list", response_model=list[CategoryOutputData])
async def get_categories(
    current_user: User = Depends(identify_user)
):
    return current_user.categories

@categories_controller.get("/item", response_model=CategoryOutputData)
async def get_category(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    category: Category | None = session.query(Category).\
        filter(
            Category.id == id,
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a category with given `id`"
        )

    return category

@categories_controller.post("/create", response_model=CategoryOutputData)
async def create_category(
    category_data: CategoryCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    category: Category = Category(
        user=current_user,
        base_category_id=category_data.base_category_id,
        name=category_data.name,
        type=category_data.type
    )

    session.add(category)
    session.commit()

    return category

@categories_controller.put("/update", response_model=CategoryOutputData)
async def update_category(
    category_data: CategoryUpdateData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    category: Category | None = session.query(Category).\
        filter(
            Category.id == category_data.id,
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a category with given `id`"
        )

    for (field, value) in category_data.dict().items():
        setattr(category, field, value)

    session.commit()

    return category

@categories_controller.delete("/delete", response_model=str)
async def delete_category(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    category: Category | None = session.query(Category).\
        filter(
            Category.id == id,
            Category.user == current_user
        ).\
        one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a category with given `id`"
        )

    session.delete(category)
    session.commit()

    return "Category was deleted"
