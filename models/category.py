from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base_model import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import CategoryType


class Category(BaseModel):
    id: Column = Column(BigInteger, primary_key=True)
    
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))
    base_category_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"))
    budget_id: Column = Column(BigInteger, ForeignKey("budget.id", ondelete="SET NULL"))

    user: RelationshipProperty = relationship("User", back_populates="categories")
    base_category: RelationshipProperty = relationship("Category", back_populates="subcategories", remote_side=lambda: Category.id)
    subcategories: RelationshipProperty = relationship("Category", back_populates="base_category")
    budget: RelationshipProperty = relationship("Budget", back_populates="categories")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="category")

    name: Column = Column(String, index=True, nullable=False)
    type: Column = Column(Enum(CategoryType, values_callable=persist_enumeration_values), nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
