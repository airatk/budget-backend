from fastapi import APIRouter, Depends, HTTPException, Query, status
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
from app.services import BudgetService, CategoryService
from models import Budget, Category, User
from models.utilities.types import BudgetType


budget_controller: APIRouter = APIRouter(prefix="/budget", tags=["budget"])


@budget_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(
    budget_type: BudgetType = Query(alias="type"),
    current_user: User = Depends(identify_user),
):
    return [budget for budget in current_user.budgets if budget.type == budget_type]

@budget_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(
    budget_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    budget_service: BudgetService = BudgetService(session=session)

    return budget_service.get_by_id(
        budget_id,
        Budget.user == current_user,
    )

@budget_controller.post("/create", response_model=BudgetOutputData, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    category_service: CategoryService = CategoryService(session=session)

    categories: list[Category] = category_service.get_list(
        or_(
            Category.id.in_(budget_data.category_ids),
            Category.base_category_id.in_(budget_data.category_ids),
        ),
        Category.user == current_user,
    )
    forbidden_category_ids: set[int] = set(budget_data.category_ids) - {category.id for category in categories}

    if forbidden_category_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "You don't have the following `category_ids`",
                "category_ids": forbidden_category_ids,
            },
        )

    budget: Budget = Budget(
        user=current_user,
        categories=categories,
        name=budget_data.name,
        type=budget_data.type,
        planned_outcomes=budget_data.planned_outcomes,
    )

    session.add(budget)
    session.commit()

    return budget

@budget_controller.patch("/update", response_model=BudgetOutputData)
async def update_budget(
    budget_data: BudgetUpdateData,
    budget_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == budget_id,
            Budget.user == current_user
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a budget with given `id`"
        )

    for (field, value) in budget_data.dict().items():
        setattr(budget, field, value)

    if budget_data.category_ids is not None:
        categories: list[Category] = [ category for category in current_user.categories if category.id in budget_data.category_ids or category.base_category_id in budget_data.category_ids ]

        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You don't have any of the provided `category_ids`"
            )

        budget.categories = categories

    session.commit()

    return budget

@budget_controller.delete("/delete", response_model=str)
async def delete_budget(
    budget_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == budget_id,
            Budget.user == current_user
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have a budget with given `id`"
        )

    session.delete(budget)
    session.commit()

    return "Budget was deleted"
