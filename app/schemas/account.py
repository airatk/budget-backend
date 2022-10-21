from datetime import date

from pydantic import BaseModel
from pydantic import Field

from app.models.account import CurrencyType


class AccountData(BaseModel):
    id: int | None
    name: str = Field(min_length=1)
    currency: CurrencyType
    openning_balance: float = 0.00

    class Config:
        orm_mode = True

class AccountBalance(BaseModel):
    account: str
    balance: float

class AccountsSummary(BaseModel):
    balance: float
    incomes: float
    outcomes: float

class DailyOutcomes(BaseModel):
    date: date
    amount: float
