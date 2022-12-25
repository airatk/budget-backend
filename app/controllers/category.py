from fastapi import APIRouter, Depends, Query, status
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
from app.utilities.exceptions import CouldNotAccessRecord, CouldNotFindRecord
from models import Category, User


category_controller: APIRouter = APIRouter(prefix="/category", tags=["category"])


@category_controller.get("/list", response_model=list[CategoryOutputData])
async def get_categories(
    current_user: User = Depends(identify_user),
):
    return current_user.categories

@category_controller.get("/item", response_model=CategoryOutputData)
async def get_category(
    category_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)
    category: Category | None = category_service.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    return category

@category_controller.post("/create", response_model=CategoryOutputData, status_code=status.HTTP_201_CREATED)
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

@category_controller.patch("/update", response_model=CategoryOutputData)
async def update_category(
    category_data: CategoryUpdateData,
    category_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)
    category: Category | None = category_service.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    return category_service.update(
        record=category,
        record_data=category_data,
    )

@category_controller.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)
    category: Category | None = category_service.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    category_service.delete(category)
