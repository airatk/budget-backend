from pydantic import NonNegativeFloat, PositiveInt

from models.utilities.types import BudgetType

from .category import CategoryOutputData
from .utilities.base import BaseData, BaseUpdateData
from .utilities.types import NonEmptyStr


class BudgetOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: NonEmptyStr
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories: list[CategoryOutputData]

class BudgetCreationData(BaseData, anystr_strip_whitespace=True):
    name: NonEmptyStr
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories_ids: list[PositiveInt]

class BudgetUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    id: PositiveInt
    name: NonEmptyStr | None
    planned_outcomes: NonNegativeFloat | None
    type: BudgetType | None
    categories_ids: list[PositiveInt] | None
