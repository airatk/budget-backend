from enum import Enum as EnumClass

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from .meta import BaseModel


class CategoryType(EnumClass):
    INCOME: str = "income"
    OUTCOME: str = "outcome"

    def __str__(self) -> str:
        return self.value

class Category(BaseModel):
    __tablename__: str = "category"

    id: Column = Column(BigInteger, primary_key=True)
    base_category_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"))
    budget_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="SET NULL"))

    base_category: RelationshipProperty = relationship("Category", back_populates="subcategories")
    budget: RelationshipProperty = relationship("Budget", back_populates="categories")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="category")

    name: Column = Column(String, index=True, nullable=False)
    type: Column = Column(Enum(CategoryType), nullable=False)
