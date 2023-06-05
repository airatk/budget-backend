from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel
from .utilities.constants import MAX_USERNAME_LENGTH


if TYPE_CHECKING:
    from .account import Account
    from .budget import Budget
    from .category import Category
    from .family import Family


class User(BaseModel):
    family_id: Mapped[int | None] = mapped_column(ForeignKey('family.id'))

    family: Mapped['Family | None'] = relationship('Family', back_populates='members', lazy='joined')
    accounts: Mapped[list['Account']] = relationship('Account', back_populates='user', cascade='all, delete', lazy='joined')
    categories: Mapped[list['Category']] = relationship('Category', back_populates='user', cascade='all, delete', lazy='joined')
    budgets: Mapped[list['Budget']] = relationship('Budget', back_populates='user', cascade='all, delete', lazy='joined')

    username: Mapped[str] = mapped_column(String(MAX_USERNAME_LENGTH), unique=True, index=True)
    password: Mapped[str]
