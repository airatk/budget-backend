from pydantic import BaseModel
from pydantic import NonNegativeFloat
from pydantic import PositiveInt

from models.utilities.types import BudgetType

from .utilities.base_models import BaseUpdateModel
from .utilities.types import NonEmptyStr
from .category import CategoryOutputData


class BudgetOutputData(BaseModel, orm_mode=True):
    id: PositiveInt
    name: NonEmptyStr
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories: list[CategoryOutputData]

class BudgetCreationData(BaseModel, anystr_strip_whitespace=True):
    name: NonEmptyStr
    planned_outcomes: NonNegativeFloat
    type: BudgetType
    categories_ids: list[PositiveInt]

class BudgetUpdateData(BaseUpdateModel, anystr_strip_whitespace=True):
    id: PositiveInt
    name: NonEmptyStr | None
    planned_outcomes: NonNegativeFloat | None
    type: BudgetType | None
    categories_ids: list[PositiveInt] | None
