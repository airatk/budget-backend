from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.schemas.budget import BudgetType
from app.schemas.budget import BudgetInputData
from app.schemas.budget import BudgetOutputData

from app.models import User
from app.models import Budget
from app.models import Category


budgets_controller: APIRouter = APIRouter(prefix="/budgets")


@budgets_controller.get("/list", response_model=list[BudgetOutputData])
async def get_budgets(type: BudgetType, current_user: User = Depends(identify_user)):
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

    return [ BudgetOutputData.from_orm(obj=budget) for budget in budgets ]

@budgets_controller.get("/item", response_model=BudgetOutputData)
async def get_budget(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
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

    return BudgetOutputData.from_orm(obj=budget)

@budgets_controller.post("/create", response_model=str)
async def create_budget(budget_data: BudgetInputData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    categories: list[Category] = [ category for category in current_user.categories if category.id in budget_data.categories_ids or category.base_category_id in budget_data.categories_ids ]

    if len(categories) == 0:
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

    return "Budget was created"

@budgets_controller.put("/update", response_model=str)
async def update_budget(budget_data: BudgetInputData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    budget: Budget | None = session.query(Budget).\
        filter(
            Budget.id == budget_data.id,
            Budget.user == current_user
        ).\
        one_or_none()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a budget with given `id`"
        )

    categories: list[Category] = [ category for category in current_user.categories if category.id in budget_data.categories_ids or category.base_category_id in budget_data.categories_ids ]

    if len(categories) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have any of the provided `categories_ids`"
        )

    budget.family = current_user.family if budget_data.type == BudgetType.JOINT else None
    budget.user = current_user if budget_data.type == BudgetType.PERSONAL else None
    budget.categories = categories
    budget.name = budget_data.name
    budget.planned_outcomes = budget_data.planned_outcomes

    session.commit()

    return "Budget was updated"

@budgets_controller.delete("/delete", response_model=str)
async def delete_budget(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
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
