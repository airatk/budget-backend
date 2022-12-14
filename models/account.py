from sqlalchemy import BigInteger, Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import RelationshipProperty, relationship

from .utilities.base import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import CurrencyType


class Account(BaseModel):
    id: Column = Column(BigInteger, primary_key=True)

    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user: RelationshipProperty = relationship("User", back_populates="accounts")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="account", passive_deletes=True)

    name: Column = Column(String, index=True, nullable=False)
    currency: Column = Column(Enum(CurrencyType, values_callable=persist_enumeration_values), nullable=False)
    openning_balance: Column = Column(Float, default=0.00, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id}, name={0.name})".format(self)
