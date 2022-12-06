from sqlalchemy import BigInteger, Column, Float, ForeignKey, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base import BaseModel


class Budget(BaseModel):
    id: Column = Column(BigInteger, primary_key=True)

    family_id: Column = Column(BigInteger, ForeignKey("family.id", ondelete="CASCADE"))
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))

    family: RelationshipProperty = relationship("Family", back_populates="budgets")
    user: RelationshipProperty = relationship("User", back_populates="budgets")
    categories: RelationshipProperty = relationship("Category", back_populates="budget")

    name: Column = Column(String, index=True, nullable=False)
    planned_outcomes: Column = Column(Float, default=0.00, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
