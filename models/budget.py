from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel


if TYPE_CHECKING:
    from .category import Category
    from .family import Family
    from .user import User


class Budget(BaseModel):
    id: int = Column(BigInteger, primary_key=True)

    family_id: int = Column(BigInteger, ForeignKey("family.id", ondelete="CASCADE"))
    user_id: int = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))

    family: "Family" = relationship("Family", back_populates="budgets")
    user: "User" = relationship("User", back_populates="budgets")
    categories: list["Category"] = relationship("Category", back_populates="budget")

    name: str = Column(String, index=True, nullable=False)
    planned_outcomes: float = Column(Float, default=0, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
