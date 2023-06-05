from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel
from .utilities.types import TransactionType


if TYPE_CHECKING:
    from .account import Account
    from .category import Category


class Transaction(BaseModel):
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    category_id: Mapped[int | None] = mapped_column(ForeignKey('category.id'))

    account: Mapped['Account'] = relationship('Account', back_populates='transactions', lazy='joined')
    category: Mapped['Category | None'] = relationship('Category', back_populates='transactions', lazy='joined')

    type: Mapped[TransactionType]
    due_date: Mapped[date]
    due_time: Mapped[time]
    amount: Mapped[float]
    note: Mapped[str] = mapped_column(default='')
