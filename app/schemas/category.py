from pydantic import BaseModel

from app.models.category import CategoryType


class CategoryData(BaseModel):
    id: int | None
    base_category_id: int | None
    name: str
    type: CategoryType

    class Config:
        orm_mode = True
