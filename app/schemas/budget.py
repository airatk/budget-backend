from pydantic import BaseModel
from pydantic import PositiveInt


class BudgetData(BaseModel):
    id: PositiveInt | None

    class Config:
        orm_mode = True
