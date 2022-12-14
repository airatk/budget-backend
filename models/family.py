from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base import BaseModel


class Family(BaseModel):
    id: Column = Column(BigInteger, primary_key=True)

    members: RelationshipProperty = relationship("User", back_populates="family")
    budgets: RelationshipProperty = relationship("Budget", back_populates="family", passive_deletes=True)

    access_code: Column = Column(String(8), unique=True, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id})".format(self)
