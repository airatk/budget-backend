from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import BudgetType


if TYPE_CHECKING:
    from .category import Category
    from .user import User


class Budget(BaseModel):
    user_id: int | None = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))

    user: Optional["User"] = relationship("User", back_populates="budgets")
    categories: list["Category"] = relationship("Category", back_populates="budget")

    name: str = Column(String, index=True, nullable=False)
    type: BudgetType = Column(Enum(BudgetType, values_callable=persist_enumeration_values), nullable=False)
    planned_outcomes: float = Column(Float, default=0, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
