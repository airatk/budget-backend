from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Enum

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from models.utilities.types import CurrencyType

from .utilities.base_model import BaseModel
from .utilities.callables import persist_enumeration_values


class Account(BaseModel):
    user_id: Column = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user: RelationshipProperty = relationship("User", back_populates="accounts")
    transactions: RelationshipProperty = relationship("Transaction", back_populates="account")

    name: Column = Column(String, index=True, nullable=False)
    currency: Column = Column(Enum(CurrencyType, values_callable=persist_enumeration_values), nullable=False)
    openning_balance: Column = Column(Float, default=0.00, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
