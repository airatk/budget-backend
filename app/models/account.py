from enum import Enum as EnumClass

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Enum

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from .meta import BaseModel
from .meta import persist_enumeration_values


class CurrencyType(str, EnumClass):
    RUB: str = "RUB"
    USD: str = "USD"

    def __repr__(self) -> str:
        return self.value

class Account(BaseModel):
    __tablename__: str = "account"

    id: Column = Column(BigInteger, primary_key=True)
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user: RelationshipProperty = relationship("User", back_populates="accounts")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="account")

    name: Column = Column(String, index=True, nullable=False)
    currency: Column = Column(Enum(CurrencyType, values_callable=persist_enumeration_values), nullable=False)
    openning_balance: Column = Column(Float, default=0.00, nullable=False)
