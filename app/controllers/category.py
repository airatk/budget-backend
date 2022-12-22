from fastapi import APIRouter, Depends, Query
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.category import (
    CategoryCreationData,
    CategoryOutputData,
    CategoryUpdateData,
)
from app.services import CategoryService
from models import Category, User


category_controller: APIRouter = APIRouter(prefix="/category", tags=["category"])


@category_controller.get("/list", response_model=list[CategoryOutputData])
async def get_categories(
    current_user: User = Depends(identify_user),
):
    return current_user.categories

@category_controller.get("/item", response_model=CategoryOutputData)
async def get_category(
    category_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    return category_service.get_by_id(
        category_id,
        Category.user == current_user,
    )

@category_controller.post("/create", response_model=CategoryOutputData)
async def create_category(
    category_data: CategoryCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    return category_service.create(
        record_data=category_data,
        user=current_user,
    )

@category_controller.put("/update", response_model=CategoryOutputData)
async def update_category(
    category_data: CategoryUpdateData,
    category_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    return category_service.update(
        category_id,
        category_data,
        Category.user == current_user,
    )

@category_controller.delete("/delete", response_model=str)
async def delete_category(
    category_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    category_service.delete(
        category_id,
        Category.user == current_user,
    )

    return "Category was deleted"
