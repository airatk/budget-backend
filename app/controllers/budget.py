from typing import Any

from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy import or_
from sqlalchemy.orm import Session

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
from core.databases.services import BudgetService


budget_controller: APIRouter = APIRouter(prefix="/budget", tags=["budget"])


@budget_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(
    budget_type: BudgetType = Query(..., alias="type"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> list[Budget]:
    budget_service: BudgetService = BudgetService(session=session)

    if budget_type is BudgetType.PERSONAL:
        return budget_service.get_list(
            Budget.type == budget_type,
            Budget.user == current_user,
        )

    if budget_type is BudgetType.JOINT:
        return budget_service.get_list(
            Budget.type == budget_type,
            or_(
                Budget.user == current_user,
                Budget.user.has(family=current_user.family),
            ),
        )

@budget_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(
    budget_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> Budget:
    budget_service: BudgetService = BudgetService(session=session)
    budget: Budget | None = budget_service.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.type is BudgetType.PERSONAL and budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    if budget.type is BudgetType.JOINT and budget.user not in current_user.family.members:
        raise CouldNotAccessRecord(budget_id, Budget)

    return budget

@budget_controller.post("/create", response_model=BudgetOutputData, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> Budget:
    categories: list[Category] = get_validated_user_categories_by_ids(
        category_ids=budget_data.category_ids,
        user=current_user,
        session=session,
    )

    budget_service: BudgetService = BudgetService(session=session)

    return budget_service.create(
        record_data=budget_data.dict(),
        user=current_user,
        categories=categories,
    )

@budget_controller.patch("/update", response_model=BudgetOutputData)
async def update_budget(
    budget_data: BudgetUpdateData,
    budget_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> Budget:
    budget_service: BudgetService = BudgetService(session=session)
    budget: Budget | None = budget_service.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    relationship_attributes: dict[str, Any] = {}

    if budget_data.category_ids is not None:
        relationship_attributes["categories"] = get_validated_user_categories_by_ids(
            category_ids=budget_data.category_ids,
            user=current_user,
            session=session,
        )

    return budget_service.update(
        record=budget,
        record_data=budget_data.dict(),
        **relationship_attributes,
    )

@budget_controller.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    budget_service: BudgetService = BudgetService(session=session)
    budget: Budget | None = budget_service.get_by_id(budget_id)

    if budget is None:
        raise CouldNotFindRecord(budget_id, Budget)

    if budget.user != current_user:
        raise CouldNotAccessRecord(budget_id, Budget)

    budget_service.delete(budget)
