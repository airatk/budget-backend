from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import CurrencyType


if TYPE_CHECKING:
    from .transaction import Transaction
    from .user import User


class Account(BaseModel):
    user_id: int = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user: "User" = relationship("User", back_populates="accounts")
    transactions: list["Transaction"] = relationship("Transaction", back_populates="account", passive_deletes=True)

    name: str = Column(String, index=True, nullable=False)
    currency: CurrencyType = Column(Enum(CurrencyType, values_callable=persist_enumeration_values), nullable=False)
    opening_balance: float = Column(Float, default=0, nullable=False)
