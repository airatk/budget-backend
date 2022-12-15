from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.budget import (
    BudgetCreationData,
    BudgetOutputData,
    BudgetUpdateData,
)
from app.services import BudgetService, CategoryService
from models import Budget, Category, User
from models.utilities.types import BudgetType


budget_controller: APIRouter = APIRouter(prefix="/budget", tags=["budget"])


@budget_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(
    budget_type: BudgetType = Query(alias="type"),
    current_user: User = Depends(identify_user),
):
    if budget_type == BudgetType.JOINT:
        return current_user.family.budgets

    if budget_type == BudgetType.PERSONAL:
        return current_user.budgets

@budget_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(
    budget_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    budget_service: BudgetService = BudgetService(session=session)

    return budget_service.get_by_id(
        budget_id,
        Budget.user == current_user or Budget.family == current_user.family,
    )

@budget_controller.post("/create", response_model=BudgetOutputData)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    categories: list[Category] = category_service.get_list(
        Category.id.in_(budget_data.categories_ids) or Category.base_category.in_(budget_data.categories_ids),
        Category.user == current_user,
    )
    forbidden_category_ids: set[int] = set(budget_data.categories_ids) - {category.id for category in categories}

    if forbidden_category_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "You don't have the following `category_ids`",
                "category_ids": forbidden_category_ids,
            },
        )

    budget: Budget = Budget(
        family=current_user.family if budget_data.type == BudgetType.JOINT else None,
        user=current_user if budget_data.type == BudgetType.PERSONAL else None,
        categories=categories,
        name=budget_data.name,
        planned_outcomes=budget_data.planned_outcomes,
    )

    session.add(budget)
    session.commit()

    return budget

@budget_controller.put("/update", response_model=BudgetOutputData)
async def update_budget(
    budget_data: BudgetUpdateData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == budget_data.id, (
                Budget.user == current_user and Budget.family.is_(None)
            ) or (
                Budget.family == current_user.family and Budget.user.is_(None)
            )
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a budget with given `id`"
        )

    for (field, value) in budget_data.dict(exclude={ "type" }).items():
        setattr(budget, field, value)

    if budget_data.categories_ids is not None:
        categories: list[Category] = [ category for category in current_user.categories if category.id in budget_data.categories_ids or category.base_category_id in budget_data.categories_ids ]

        if categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have any of the provided `categories_ids`"
            )

        budget.categories = categories

    if budget_data.type is not None:
        budget.family = current_user.family if budget_data.type == BudgetType.JOINT else None
        budget.user = current_user if budget_data.type == BudgetType.PERSONAL else None

    session.commit()

    return budget

@budget_controller.delete("/delete", response_model=str)
async def delete_budget(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == id,
            Budget.user == current_user
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a budget with given `id`"
        )

    session.delete(budget)
    session.commit()

    return "Budget was deleted"
