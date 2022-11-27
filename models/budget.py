from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .utilities.base_model import BaseModel


class Budget(BaseModel):
    family_id: Column = Column(BigInteger, ForeignKey("family.id", ondelete="CASCADE"))
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))

    family: RelationshipProperty = relationship("Family", back_populates="budgets")
    user: RelationshipProperty = relationship("User", back_populates="budgets")
    categories: RelationshipProperty = relationship("Category", back_populates="budget")

    name: Column = Column(String, index=True, nullable=False)
    planned_outcomes: Column = Column(Float, default=0.00, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
