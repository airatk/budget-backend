from pydantic import BaseModel


class BudgetData(BaseModel):
    id: int | None

    class Config:
        orm_mode = True
