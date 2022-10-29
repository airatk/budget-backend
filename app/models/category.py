from enum import Enum as EnumClass

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Enum

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .meta import BaseModel
from .meta import persist_enumeration_values


class CategoryType(str, EnumClass):
    INCOME: str = "Income"
    OUTCOME: str = "Outcome"

    def __repr__(self) -> str:
        return self.value

class Category(BaseModel):
    __tablename__: str = "category"

    id: Column = Column(BigInteger, primary_key=True)
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))
    base_category_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"))
    budget_id: Column = Column(BigInteger, ForeignKey("budget.id", ondelete="SET NULL"))

    user: RelationshipProperty = relationship("User", back_populates="categories")
    base_category: RelationshipProperty = relationship("Category", back_populates="subcategories", remote_side=id)
    subcategories: RelationshipProperty = relationship("Category", back_populates="base_category")
    budget: RelationshipProperty = relationship("Budget", back_populates="categories")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="category")

    name: Column = Column(String, index=True, nullable=False)
    type: Column = Column(Enum(CategoryType, values_callable=persist_enumeration_values), nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
