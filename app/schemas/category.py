from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt

from app.models.category import CategoryType


class CategoryData(BaseModel):
    id: PositiveInt | None
    base_category_id: PositiveInt | None
    name: str = Field(min_length=1)
    type: CategoryType

    class Config:
        orm_mode = True
