from enum import Enum

from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from pydantic import NonNegativeFloat
from pydantic import NonPositiveFloat

from app.models.account import CurrencyType


class SummaryPeriodType(str, Enum):
    CURRENT_MONTH: str = "Current Month"
    CURRENT_YEAR: str = "Current Year"
    ALL_TIME: str = "All Time"

    def __repr__(self):
        return self.value


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
    balance: float = 0.00
    incomes: NonNegativeFloat
    outcomes: NonPositiveFloat

class PeriodSummary(BaseModel):
    period: SummaryPeriodType
    accounts_summary: AccountsSummary

class DailyHighlight(BaseModel):
    date: date
    amount: NonNegativeFloat

class TrendPoint(BaseModel):
    date: date
    current_month_amount: NonNegativeFloat
    average_amount: NonNegativeFloat

    class Config:
        orm_mode = True
