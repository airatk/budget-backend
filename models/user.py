from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base import BaseModel


MAX_USERNAME_LENGTH: int = 30


class User(BaseModel):
    id: Column = Column(BigInteger, primary_key=True)

    family_id: Column = Column(BigInteger, ForeignKey("family.id", ondelete="SET NULL"))

    family: RelationshipProperty = relationship("Family", back_populates="members")
    accounts: RelationshipProperty = relationship("Account", back_populates="user")
    categories: RelationshipProperty = relationship("Category", back_populates="user")
    budgets: RelationshipProperty = relationship("Budget", back_populates="user")

    username: Column = Column(String(MAX_USERNAME_LENGTH), unique=True, index=True, nullable=False)
    password: Column = Column(String, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, username={0.username})".format(self)
