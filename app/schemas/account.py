from datetime import date

from pydantic import Field, NonNegativeFloat, NonPositiveFloat, PositiveInt

from models.account import CurrencyType
from models.utilities.types import SummaryPeriodType

from .utilities.base import BaseData, BaseUpdateData


class AccountOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: str
    currency: CurrencyType
    openning_balance: int = 0

class AccountCreationData(BaseData, anystr_strip_whitespace=True):
    name: str = Field(..., min_length=1)
    currency: CurrencyType
    openning_balance: int = 0

class AccountUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    name: str | None = Field(None, min_length=1)
    currency: CurrencyType | None
    openning_balance: int | None


class AccountBalanceData(BaseData):
    account: str
    balance: float

class PeriodSummaryData(BaseData):
    period: SummaryPeriodType
    balance: float = 0
    incomes: NonNegativeFloat
    outcomes: NonPositiveFloat

class DailyHighlightData(BaseData):
    date: date
    amount: NonNegativeFloat

class TrendPointData(BaseData):
    date: date
    current_month_amount: NonNegativeFloat
    average_amount: NonNegativeFloat
