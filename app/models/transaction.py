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
from sqlalchemy.orm.relationships import RelationshipProperty

from .meta import BaseModel


class TransactionType(EnumClass):
    INCOME: str = "income"
    OUTCOME: str = "outcome"
    TRANSFER: str = "transfer"

    def __str__(self) -> str:
        return self.value

class Transaction(BaseModel):
    __tablename__: str = "transaction"

    id: Column = Column(BigInteger, primary_key=True)
    account_id: Column = Column(BigInteger, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    category_id: Column = Column(BigInteger, ForeignKey("category.id", ondelete="SET NULL"))

    account: RelationshipProperty = relationship("Account", back_populates="transations")
    category: RelationshipProperty = relationship("Category", back_populates="transations")

    type: Column = Column(Enum(TransactionType), nullable=False)
    due_date: Column = Column(Date, nullable=False)
    due_time: Column = Column(Time, nullable=False)
    amount: Column = Column(Float, nullable=False)
    note: Column = Column(String, default="", nullable=False)
