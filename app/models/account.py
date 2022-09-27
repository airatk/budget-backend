from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from .meta import BaseModel


class Account(BaseModel):
    __tablename__: str = "account"

    id: Column = Column(BigInteger, primary_key=True)
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user: RelationshipProperty = relationship("User", back_populates="accounts")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="account")

    name: Column = Column(String, index=True, nullable=False)
    currency: Column = Column(String, nullable=False)
    openning_balance: Column = Column(Float, default=0.00, nullable=False)
