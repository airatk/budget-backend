from datetime import date
from typing import Any, cast

from pydantic import Field, NonNegativeFloat, PositiveInt, validator

from core.databases.models.account import CurrencyType
from core.databases.models.utilities.types import SummaryPeriodType

from .utilities.base import BaseData, BaseUpdateData


class AccountOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: str
    currency: CurrencyType
    opening_balance: int = 0

class AccountCreationData(BaseData, anystr_strip_whitespace=True):
    name: str = Field(..., min_length=1)
    currency: CurrencyType
    opening_balance: int = 0

class AccountUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    name: str | None = Field(None, min_length=1)
    currency: CurrencyType | None
    opening_balance: int | None


class AccountBalanceData(BaseData):
    account: str
    balance: float

class PeriodSummaryData(BaseData):
    period: SummaryPeriodType
    incomes: NonNegativeFloat
    outcomes: NonNegativeFloat
    balance: float = 0

    @validator('balance', pre=True)
    def calculate_balance(cls, value: Any, values: dict[str, Any]) -> float:
        return cast(float, value or (values['incomes'] - values['outcomes']))

class DailyHighlightData(BaseData):
    date: date
    amount: NonNegativeFloat

class TrendPointData(BaseData):
    date: date
    current_amount: NonNegativeFloat
    average_amount: NonNegativeFloat
