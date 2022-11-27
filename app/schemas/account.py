from datetime import date

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import NonNegativeFloat
from pydantic import NonPositiveFloat

from models.account import CurrencyType
from models.utilities.types import SummaryPeriodType

from .utilities.base_models import BaseUpdateModel
from .utilities.types import NonEmptyStr


class AccountOutputData(BaseModel, orm_mode=True):
    id: PositiveInt
    name: str
    currency: CurrencyType
    openning_balance: NonNegativeFloat = 0.00

class AccountCreationData(BaseModel, anystr_strip_whitespace=True):
    name: NonEmptyStr
    currency: CurrencyType
    openning_balance: NonNegativeFloat = 0.00

class AccountUpdateData(BaseUpdateModel, anystr_strip_whitespace=True):
    id: PositiveInt
    name: NonEmptyStr | None
    currency: CurrencyType | None
    openning_balance: NonNegativeFloat | None


class AccountBalanceData(BaseModel):
    account: str
    balance: float

class AccountsSummaryData(BaseModel):
    balance: float = 0.00
    incomes: NonNegativeFloat
    outcomes: NonPositiveFloat

class PeriodSummaryData(BaseModel):
    period: SummaryPeriodType
    accounts_summary: AccountsSummaryData

class DailyHighlightData(BaseModel):
    date: date
    amount: NonNegativeFloat

class TrendPointData(BaseModel):
    date: date
    current_month_amount: NonNegativeFloat
    average_amount: NonNegativeFloat
