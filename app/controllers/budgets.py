from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.budget import (
    BudgetCreationData,
    BudgetOutputData,
    BudgetType,
    BudgetUpdateData
)
from models import Budget, Category, User


budgets_controller: APIRouter = APIRouter(prefix="/budgets")


@budgets_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(
    type: BudgetType,
    current_user: User = Depends(identify_user)
):
    budgets: list[Budget]

    if type == BudgetType.JOINT:
        budgets = current_user.family.budgets
    elif type == BudgetType.PERSONAL:
        budgets = current_user.budgets
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided `budget_type` is wrong"
        )

    return budgets

@budgets_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == id,
            Budget.user == current_user or Budget.family == current_user.family
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a budget with given `id`"
        )

    return budget

@budgets_controller.post("/create", response_model=BudgetOutputData)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    categories: list[Category] = [ category for category in current_user.categories if category.id in budget_data.categories_ids or category.base_category_id in budget_data.categories_ids ]

    if categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have any of the provided `categories_ids`"
        )

    budget: Budget = Budget(
        family=current_user.family if budget_data.type == BudgetType.JOINT else None,
        user=current_user if budget_data.type == BudgetType.PERSONAL else None,
        categories=categories,
        name=budget_data.name,
        planned_outcomes=budget_data.planned_outcomes
    )

    session.add(budget)
    session.commit()

    return budget

@budgets_controller.put("/update", response_model=BudgetOutputData)
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

@budgets_controller.delete("/delete", response_model=str)
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
