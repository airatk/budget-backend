from typing import Any

from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.budget import (
    BudgetCreationData,
    BudgetOutputData,
    BudgetUpdateData,
)
from app.services import BudgetService
from app.utilities.exceptions import CouldNotAccessRecord, CouldNotFindRecord
from models import Budget, Category, User
from models.utilities.types import BudgetType

from .utilities.callables import get_validated_user_categories_by_ids


budget_controller: APIRouter = APIRouter(prefix="/budget", tags=["budget"])


@budget_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(
    budget_type: BudgetType = Query(..., alias="type"),
    current_user: User = Depends(identify_user),
):
    return [budget for budget in current_user.budgets if budget.type == budget_type]

@budget_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(
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

    return budget

@budget_controller.post("/create", response_model=BudgetOutputData, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    categories: list[Category] = get_validated_user_categories_by_ids(
        category_ids=budget_data.category_ids,
        user=current_user,
        session=session,
    )

    budget_service: BudgetService = BudgetService(session=session)

    return budget_service.create(
        record_data=budget_data,
        user=current_user,
        categories=categories,
    )

@budget_controller.patch("/update", response_model=BudgetOutputData)
async def update_budget(
    budget_data: BudgetUpdateData,
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

    relationship_attributes: dict[str, Any] = {}

    if budget_data.category_ids is not None:
        relationship_attributes["categories"] = get_validated_user_categories_by_ids(
            category_ids=budget_data.category_ids,
            user=current_user,
            session=session,
        )

    return budget_service.update(
        record=budget,
        record_data=budget_data,
        **relationship_attributes,
    )

@budget_controller.delete("/delete", response_model=str)
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

    return "Budget was deleted"
