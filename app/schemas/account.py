from datetime import date

from pydantic import NonNegativeFloat, NonPositiveFloat, PositiveInt

from models.account import CurrencyType
from models.utilities.types import SummaryPeriodType

from .utilities.base import BaseData, BaseUpdateData
from .utilities.types import NonEmptyStr


class AccountOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: str
    currency: CurrencyType
    openning_balance: NonNegativeFloat = 0.00

class AccountCreationData(BaseData, anystr_strip_whitespace=True):
    name: NonEmptyStr
    currency: CurrencyType
    openning_balance: NonNegativeFloat = 0.00

class AccountUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    id: PositiveInt
    name: NonEmptyStr | None
    currency: CurrencyType | None
    openning_balance: NonNegativeFloat | None


class AccountBalanceData(BaseData):
    account: str
    balance: float

class AccountsSummaryData(BaseData):
    balance: float = 0.00
    incomes: NonNegativeFloat
    outcomes: NonPositiveFloat

class PeriodSummaryData(BaseData):
    period: SummaryPeriodType
    accounts_summary: AccountsSummaryData

class DailyHighlightData(BaseData):
    date: date
    amount: NonNegativeFloat

class TrendPointData(BaseData):
    date: date
    current_month_amount: NonNegativeFloat
    average_amount: NonNegativeFloat
