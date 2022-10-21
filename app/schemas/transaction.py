from datetime import date
from datetime import time

from pydantic import BaseModel
from pydantic import PositiveFloat

from app.models.transaction import TransactionType


class TransactionData(BaseModel):
    id: int | None
    account_id: int
    category_id: int
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str = ""

    class Config:
        orm_mode = True

class TransactionsPeriod(BaseModel):
    month: int
    year: int
