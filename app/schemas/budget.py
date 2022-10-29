from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from pydantic import NonNegativeFloat
from pydantic import PositiveInt

from .category import CategoryData


class BudgetType(str, Enum):
    JOINT: str = "joint"
    PERSONAL: str = "personal"

    def __repr__(self) -> str:
        return self.value

class BudgetData(BaseModel):
    id: PositiveInt | None
    name: str = Field(min_length=1)
    planned_outcomes: NonNegativeFloat

class BudgetInputData(BudgetData):
    type: BudgetType
    categories_ids: list[PositiveInt]

class BudgetOutputData(BudgetData):
    categories: list[CategoryData]

    class Config:
        orm_mode = True
