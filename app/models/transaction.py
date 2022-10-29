from enum import Enum as EnumClass

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Enum

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .meta import BaseModel
from .meta import persist_enumeration_values


class TransactionType(str, EnumClass):
    INCOME: str = "Income"
    OUTCOME: str = "Outcome"
    TRANSFER: str = "Transfer"

    def __repr__(self) -> str:
        return self.value

class Transaction(BaseModel):
    __tablename__: str = "transaction"

    id: Column = Column(BigInteger, primary_key=True)
    account_id: Column = Column(BigInteger, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    category_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="SET NULL"))

    account: RelationshipProperty = relationship("Account", back_populates="transactions")
    category: RelationshipProperty = relationship("Category", back_populates="transactions")

    type: Column = Column(Enum(TransactionType, values_callable=persist_enumeration_values), nullable=False)
    due_date: Column = Column(Date, nullable=False)
    due_time: Column = Column(Time, nullable=False)
    amount: Column = Column(Float, nullable=False)
    note: Column = Column(String, default="", nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, amount={self.amount})"
