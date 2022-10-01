from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


transactions_controller: APIRouter = APIRouter(prefix="/transactions")


class Period(BaseModel):
    month: int
    year: int

class TransactionData(BaseModel):
    id: int | None


@transactions_controller.get("/periods")
async def get_periods(current_user: User = Depends(identify_user)):
    pass

@transactions_controller.get("/list")
async def get_transactions(period: Period, current_user: User = Depends(identify_user)):
    pass

@transactions_controller.get("/item")
async def get_transaction(id: int, current_user: User = Depends(identify_user)):
    pass

@transactions_controller.post("/create")
async def create_transaction(transaction_data: TransactionData, current_user: User = Depends(identify_user)):
    pass

@transactions_controller.put("/update")
async def update_transaction(transaction_data: TransactionData, current_user: User = Depends(identify_user)):
    pass

@transactions_controller.delete("/delete")
async def delete_transaction(id: int, current_user: User = Depends(identify_user)):
    pass
