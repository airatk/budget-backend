from pydantic import Field, NonNegativeFloat, PositiveInt

from models.utilities.types import BudgetType

from .category import CategoryOutputData
from .utilities.base import BaseData, BaseUpdateData


class BudgetOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: str = Field(..., min_length=1)
    planned_outcomes: NonNegativeFloat
    categories: list[CategoryOutputData]

class BudgetCreationData(BaseData, anystr_strip_whitespace=True):
    name: str = Field(..., min_length=1)
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories_ids: list[PositiveInt] = Field(..., min_items=1)

class BudgetUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    name: str | None = Field(None, min_length=1)
    planned_outcomes: NonNegativeFloat | None
    type: BudgetType | None
    categories_ids: list[PositiveInt] | None = Field(None, min_items=1)
