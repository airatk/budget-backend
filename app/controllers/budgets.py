from pydantic import BaseModel

from fastapi import APIRouter


budgets_controller: APIRouter = APIRouter(prefix="/budgets")


class BudgetData(BaseModel):
    id: int | None


@budgets_controller.get("/list")
async def get_budgets():
    pass

@budgets_controller.get("/item")
async def get_budget(id: int):
    pass

@budgets_controller.post("/create")
async def create_budget(budget_data: BudgetData):
    pass

@budgets_controller.put("/update")
async def update_budget(budget_data: BudgetData):
    pass

@budgets_controller.delete("/delete")
async def delete_budget(id: int):
    pass
