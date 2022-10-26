from datetime import date
from datetime import time

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import PositiveFloat

from app.models.transaction import TransactionType


class TransactionData(BaseModel):
    id: PositiveInt | None
    account_id: PositiveInt
    category_id: PositiveInt
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str = ""

    class Config:
        orm_mode = True

class TransactionsPeriod(BaseModel):
    month: PositiveInt
    year: PositiveInt
