from sqlalchemy import Column, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base_model import BaseModel


class Family(BaseModel):
    members: RelationshipProperty = relationship("User", back_populates="family")
    budgets: RelationshipProperty = relationship("Budget", back_populates="family")

    access_code: Column = Column(String(8), unique=True, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id})".format(self)
