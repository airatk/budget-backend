from pydantic import BaseModel, PositiveInt

from models.category import CategoryType

from .utilities.base_models import BaseUpdateModel
from .utilities.types import NonEmptyStr


class CategoryOutputData(BaseModel, orm_mode=True):
    id: PositiveInt
    base_category_id: PositiveInt | None
    name: NonEmptyStr
    type: CategoryType

class CategoryCreationData(BaseModel, anystr_strip_whitespace=True):
    base_category_id: PositiveInt | None
    name: NonEmptyStr
    type: CategoryType

class CategoryUpdateData(BaseUpdateModel, anystr_strip_whitespace=True):
    id: PositiveInt
    base_category_id: PositiveInt | None
    name: NonEmptyStr | None
    type: CategoryType | None
