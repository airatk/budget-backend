from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.category import (
    CategoryCreationData,
    CategoryOutputData,
    CategoryUpdateData,
)
from app.utilities.exceptions.records import (
    CouldNotAccessRecord,
    CouldNotFindRecord,
)
from core.databases.models import Category, User
from core.databases.repositories import CategoryRepository


category_router: APIRouter = APIRouter(prefix='/category', tags=['category'])


@category_router.get('/list', response_model=list[CategoryOutputData])
async def get_categories(
    current_user: User = Depends(identify_user),
) -> list[Category]:
    return current_user.categories

@category_router.get('/item', response_model=CategoryOutputData)
async def get_category(
    category_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Category:
    category_repository: CategoryRepository = CategoryRepository(session=session)
    category: Category | None = await category_repository.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    return category

@category_router.post('/create', response_model=CategoryOutputData, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreationData,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Category:
    category_repository: CategoryRepository = CategoryRepository(session=session)

    return await category_repository.create(
        record_data=category_data.dict(),
        user=current_user,
    )

@category_router.patch('/update', response_model=CategoryOutputData)
async def update_category(
    category_data: CategoryUpdateData,
    category_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Category:
    category_repository: CategoryRepository = CategoryRepository(session=session)
    category: Category | None = await category_repository.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    return await category_repository.update(
        record=category,
        record_data=category_data.dict(),
    )

@category_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> None:
    category_repository: CategoryRepository = CategoryRepository(session=session)
    category: Category | None = await category_repository.get_by_id(category_id)

    if category is None:
        raise CouldNotFindRecord(category_id, Category)

    if category.user != current_user:
        raise CouldNotAccessRecord(category_id, Category)

    await category_repository.delete(category)
