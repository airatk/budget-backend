from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .meta import BaseModel


class User(BaseModel):
    __tablename__: str = "user"

    id: Column = Column(BigInteger, primary_key=True)
    family_id: Column = Column(BigInteger, ForeignKey("family.id", ondelete="SET NULL"))

    family: RelationshipProperty = relationship("Family", back_populates="members")
    accounts: RelationshipProperty = relationship("Account", back_populates="user")
    categories: RelationshipProperty = relationship("Category", back_populates="user")
    budgets: RelationshipProperty = relationship("Budget", back_populates="user")

    username: Column = Column(String(30), unique=True, index=True, nullable=False)
    password: Column = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"
