from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    String,
    Time,
)
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel
from .utilities.callables import persist_enumeration_values
from .utilities.types import TransactionType


if TYPE_CHECKING:
    from .account import Account
    from .category import Category


class Transaction(BaseModel):
    account_id: int = Column(BigInteger, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    category_id: int = Column(BigInteger, ForeignKey('category.id', ondelete='SET NULL'))

    account: 'Account' = relationship('Account', back_populates='transactions')
    category: 'Category' = relationship('Category', back_populates='transactions')

    type: TransactionType = Column(Enum(TransactionType, values_callable=persist_enumeration_values), nullable=False)
    due_date: date = Column(Date, nullable=False)
    due_time: time = Column(Time, nullable=False)
    amount: float = Column(Float, nullable=False)
    note: str = Column(String, default='', nullable=False)
