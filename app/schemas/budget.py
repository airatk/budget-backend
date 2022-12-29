from typing import Any

from pydantic import Field, NonNegativeFloat, PositiveInt

from core.databases.models.utilities.types import BudgetType

from .category import CategoryOutputData
from .utilities.base import BaseData, BaseUpdateData


class BudgetOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    name: str = Field(..., min_length=1)
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories: list[CategoryOutputData]

class BudgetInputData(BaseData, anystr_strip_whitespace=True):
    def dict(self, **keyword_arguments) -> dict[str, Any]:
        keyword_arguments["exclude"] = {"category_ids"}

        return super().dict(**keyword_arguments)

class BudgetCreationData(BudgetInputData):
    name: str = Field(..., min_length=1)
    planned_outcomes: NonNegativeFloat
    type: BudgetType

    category_ids: list[PositiveInt] = Field(..., min_items=1)

class BudgetUpdateData(BaseUpdateData, BudgetInputData):
    name: str | None = Field(None, min_length=1)
    planned_outcomes: NonNegativeFloat | None
    type: BudgetType | None

    category_ids: list[PositiveInt] | None = Field(None, min_items=1)
