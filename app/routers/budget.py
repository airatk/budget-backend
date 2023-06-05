from typing import Any

from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.budget import (
    BudgetCreationData,
    BudgetOutputData,
    BudgetUpdateData,
)
from app.utilities.callables import get_validated_user_categories_by_ids
from app.utilities.exceptions.records import (
    CouldNotAccessRecord,
    CouldNotFindRecord,
)
from core.databases.models import Budget, Category, User
from core.databases.models.utilities.types import BudgetType
from core.databases.repositories import BudgetRepository


budget_router: APIRouter = APIRouter(prefix='/budget', tags=['budget'])


@budget_router.get('/list', response_model=list[BudgetOutputData])
async def get_budgets(
    budget_type: BudgetType = Query(..., alias='type'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[Budget]:
    budget_repository: BudgetRepository = BudgetRepository(session=session)

    if budget_type is BudgetType.PERSONAL:
        return await budget_repository.get_list(
            Budget.type == budget_type,
            Budget.user == current_user,
        )

    if budget_type is BudgetType.JOINT:
        return await budget_repository.get_list(
            Budget.type == budget_type,
            or_(
                Budget.user == current_user,
                Budget.user.has(family=current_user.family),
            ),
        )

@budget_router.get('/item', response_model=BudgetOutputData)
async def get_budget(
    budget_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Budget:
    budget_repository: BudgetRepository = BudgetRepository(session=session)
    budget: Budget | None = await budget_repository.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.type is BudgetType.PERSONAL and budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    if budget.type is BudgetType.JOINT and (current_user.family is None or budget.user not in current_user.family.members):
        raise CouldNotAccessRecord(budget_id, Budget)

    return budget

@budget_router.post('/create', response_model=BudgetOutputData, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Budget:
    categories: list[Category] = await get_validated_user_categories_by_ids(
        category_ids=budget_data.category_ids,
        user=current_user,
        session=session,
    )

    budget_repository: BudgetRepository = BudgetRepository(session=session)

    return await budget_repository.create(
        record_data=budget_data.dict(),
        user=current_user,
        categories=categories,
    )

@budget_router.patch('/update', response_model=BudgetOutputData)
async def update_budget(
    budget_data: BudgetUpdateData,
    budget_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Budget:
    budget_repository: BudgetRepository = BudgetRepository(session=session)
    budget: Budget | None = await budget_repository.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    relationship_attributes: dict[str, Any] = {}

    if budget_data.category_ids is not None:
        relationship_attributes['categories'] = get_validated_user_categories_by_ids(
            category_ids=budget_data.category_ids,
            user=current_user,
            session=session,
        )

    return await budget_repository.update(
        record=budget,
        record_data=budget_data.dict(),
        **relationship_attributes,
    )

@budget_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> None:
    budget_repository: BudgetRepository = BudgetRepository(session=session)
    budget: Budget | None = await budget_repository.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    await budget_repository.delete(budget)
