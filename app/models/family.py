from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import String

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .meta import BaseModel


class Family(BaseModel):
    __tablename__: str = "family"

    id: Column = Column(BigInteger, primary_key=True)

    members: RelationshipProperty = relationship("User", back_populates="family")
    budgets: RelationshipProperty = relationship("Budget", back_populates="family")

    access_code: Column = Column(String(8), unique=True, nullable=False)
