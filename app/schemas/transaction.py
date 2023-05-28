from datetime import date, time

from pydantic import PositiveFloat, PositiveInt

from core.databases.models.utilities.types import TransactionType

from .utilities.base import BaseData, BaseUpdateData
from .utilities.types import Month, Year


class TransactionOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    account_id: PositiveInt
    category_id: PositiveInt
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str

class TransactionCreationData(BaseData, anystr_strip_whitespace=True):
    account_id: PositiveInt
    category_id: PositiveInt
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str = ''

class TransactionUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    account_id: PositiveInt | None
    category_id: PositiveInt | None
    type: TransactionType | None
    due_date: date | None
    due_time: time | None
    amount: PositiveFloat | None
    note: str | None


class TransactionsPeriodData(BaseData):
    year: Year
    month: Month
