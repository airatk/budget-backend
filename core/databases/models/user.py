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

    family: Mapped['Family | None'] = relationship(back_populates='members', lazy='selectin')
    accounts: Mapped[list['Account']] = relationship(back_populates='user', cascade='all, delete', lazy='selectin')
    categories: Mapped[list['Category']] = relationship(back_populates='user', cascade='all, delete', lazy='selectin')
    budgets: Mapped[list['Budget']] = relationship(back_populates='user', cascade='all, delete', lazy='selectin')

    username: Mapped[str] = mapped_column(String(MAX_USERNAME_LENGTH), unique=True, index=True)
    password: Mapped[str]
