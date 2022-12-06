from pydantic import PositiveInt

from models.category import CategoryType

from .utilities.base import BaseData, BaseUpdateData
from .utilities.types import NonEmptyStr


class CategoryOutputData(BaseData, orm_mode=True):
    id: PositiveInt
    base_category_id: PositiveInt | None
    name: NonEmptyStr
    type: CategoryType

class CategoryCreationData(BaseData, anystr_strip_whitespace=True):
    base_category_id: PositiveInt | None
    name: NonEmptyStr
    type: CategoryType

class CategoryUpdateData(BaseUpdateData, anystr_strip_whitespace=True):
    id: PositiveInt
    base_category_id: PositiveInt | None
    name: NonEmptyStr | None
    type: CategoryType | None
