from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from pydantic import NonNegativeFloat

from app.models.account import CurrencyType


class AccountData(BaseModel):
    id: PositiveInt | None
    name: str = Field(min_length=1)
    currency: CurrencyType
    openning_balance: NonNegativeFloat = 0.00

    class Config:
        orm_mode = True

class AccountBalance(BaseModel):
    account: str
    balance: float

class AccountsSummary(BaseModel):
    balance: float
    incomes: float
    outcomes: float

class DailyHighlight(BaseModel):
    date: date
    amount: NonNegativeFloat
