from typing import NamedTuple, Type

from core.databases.models import (
    Account,
    Budget,
    Category,
    Family,
    Transaction,
    User,
)
from core.databases.models.utilities.base import BaseModel


class DatabaseMappingItem(NamedTuple):
    model: Type[BaseModel]
    file_name: str
    sequence_id: str


GENERIC_JSON_FILE_PATH: str = 'tests/mock/data/{0}.json'

DATABASE_MAPPING: tuple[DatabaseMappingItem, ...] = (
    DatabaseMappingItem(model=Family, file_name='families', sequence_id='family_id_seq'),
    DatabaseMappingItem(model=User, file_name='users', sequence_id='user_id_seq'),
    DatabaseMappingItem(model=Budget, file_name='budgets', sequence_id='budget_id_seq'),
    DatabaseMappingItem(model=Category, file_name='categories', sequence_id='category_id_seq'),
    DatabaseMappingItem(model=Account, file_name='accounts', sequence_id='account_id_seq'),
    DatabaseMappingItem(model=Transaction, file_name='transactions', sequence_id='transaction_id_seq'),
)
