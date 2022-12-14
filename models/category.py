from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import CategoryType


if TYPE_CHECKING:
    from .user import User
    from .budget import Budget
    from .transaction import Transaction


class Category(BaseModel):
    id: int = Column(BigInteger, primary_key=True)

    user_id: int = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    base_category_id: int = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"))
    budget_id: int = Column(BigInteger, ForeignKey("budget.id", ondelete="SET NULL"))

    user: "User" = relationship("User", back_populates="categories")
    base_category: "Category" = relationship("Category", back_populates="subcategories", remote_side=lambda: Category.id)
    subcategories: list["Category"] = relationship("Category", back_populates="base_category", passive_deletes=True)
    budget: "Budget" = relationship("Budget", back_populates="categories")
    transactions: list["Transaction"] = relationship("Transaction", back_populates="category")

    name: str = Column(String, index=True, nullable=False)
    type: CategoryType = Column(Enum(CategoryType, values_callable=persist_enumeration_values), nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
