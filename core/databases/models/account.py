from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel
from .utilities.types import CurrencyType


if TYPE_CHECKING:
    from .transaction import Transaction
    from .user import User


class Account(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='accounts', lazy='selectin')
    transactions: Mapped[list['Transaction']] = relationship(back_populates='account', cascade='all, delete', lazy='selectin')

    name: Mapped[str] = mapped_column(index=True)
    currency: Mapped[CurrencyType]
    opening_balance: Mapped[float] = mapped_column(default=0)
