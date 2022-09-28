from pydantic import BaseModel

from fastapi import APIRouter


transactions_controller: APIRouter = APIRouter(prefix="/transactions")


class Period(BaseModel):
    month: int
    year: int

class TransactionData(BaseModel):
    id: int | None


@transactions_controller.get("/periods")
async def get_periods():
    pass

@transactions_controller.get("/list")
async def get_transactions(period: Period):
    pass

@transactions_controller.get("/item")
async def get_transaction(id: int):
    pass

@transactions_controller.post("/create")
async def create_transaction(transaction_data: TransactionData):
    pass

@transactions_controller.put("/update")
async def update_transaction(transaction_data: TransactionData):
    pass

@transactions_controller.delete("/delete")
async def delete_transaction(id: int):
    pass
