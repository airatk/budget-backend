from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from .meta import BaseModel


class Budget(BaseModel):
    __tablename__: str = "budget"

    id: Column = Column(BigInteger, primary_key=True)
    family_id: Column = Column(BigInteger, ForeignKey("family.id", ondelete="CASCADE"))
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"))

    family: RelationshipProperty = relationship("Family", back_populates="budgets")
    user: RelationshipProperty = relationship("User", back_populates="budgets")
    categories: RelationshipProperty = relationship("Category", back_populates="budget")

    name: Column = Column(String, index=True, nullable=False)
    planned_outcomes: Column = Column(Float, default=0.00, nullable=False)
