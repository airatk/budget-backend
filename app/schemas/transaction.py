from datetime import date, time

from pydantic import BaseModel, PositiveFloat, PositiveInt

from models.utilities.types import TransactionType


class TransactionOutputData(BaseModel, orm_mode=True):
    id: PositiveInt
    account_id: PositiveInt
    category_id: PositiveInt
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str

class TransactionCreationData(BaseModel, anystr_strip_whitespace=True):
    account_id: PositiveInt
    category_id: PositiveInt
    type: TransactionType
    due_date: date
    due_time: time
    amount: PositiveFloat
    note: str = ""

class TransactionUpdateData(BaseModel, anystr_strip_whitespace=True):
    id: PositiveInt
    account_id: PositiveInt | None
    category_id: PositiveInt | None
    type: TransactionType | None
    due_date: date | None
    due_time: time | None
    amount: PositiveFloat | None
    note: str | None


class TransactionsPeriod(BaseModel):
    month: PositiveInt
    year: PositiveInt
