from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


budgets_controller: APIRouter = APIRouter(prefix="/budgets")


class BudgetData(BaseModel):
    id: int | None


@budgets_controller.get("/list")
async def get_budgets(current_user: User = Depends(identify_user)):
    pass

@budgets_controller.get("/item")
async def get_budget(id: int, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.post("/create")
async def create_budget(budget_data: BudgetData, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.put("/update")
async def update_budget(budget_data: BudgetData, current_user: User = Depends(identify_user)):
    pass

@budgets_controller.delete("/delete")
async def delete_budget(id: int, current_user: User = Depends(identify_user)):
    pass
