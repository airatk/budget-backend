from pydantic import Field, PositiveInt

from models.category import CategoryType

from .utilities.base import BaseData, BaseUpdateData


class CategoryOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    base_category_id: PositiveInt | None
    name: str = Field(..., min_length=1)
    type: CategoryType

class CategoryCreationData(BaseData, anystr_strip_whitespace=True):
    base_category_id: PositiveInt | None
    name: str = Field(..., min_length=1)
    type: CategoryType

class CategoryUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    base_category_id: PositiveInt | None
    name: str | None = Field(None, min_length=1)
    type: CategoryType | None
