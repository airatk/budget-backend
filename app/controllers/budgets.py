from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.schemas.budget import BudgetData

from app.models import User


budgets_controller: APIRouter = APIRouter(prefix="/budgets")


@budgets_controller.get("/list", response_model=list[BudgetData])
async def get_budgets(current_user: User = Depends(identify_user)):
    pass

@budgets_controller.get("/item", response_model=BudgetData)
async def get_budget(id: int, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.post("/create", response_model=str)
async def create_budget(budget_data: BudgetData, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.put("/update", response_model=str)
async def update_budget(budget_data: BudgetData, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.delete("/delete", response_model=str)
async def delete_budget(id: int, current_user: User = Depends(identify_user)):
    pass
