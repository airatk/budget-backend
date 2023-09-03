from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel
from .utilities.types import CategoryType


if TYPE_CHECKING:
    from .budget import Budget
    from .transaction import Transaction
    from .user import User


class Category(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    base_category_id: Mapped[int | None] = mapped_column(ForeignKey('category.id'))
    budget_id: Mapped[int | None] = mapped_column(ForeignKey('budget.id'))

    user: Mapped['User'] = relationship(back_populates='categories', lazy='selectin')
    base_category: Mapped['Category | None'] = relationship(back_populates='subcategories', lazy='selectin', remote_side=lambda: Category.id)
    subcategories: Mapped[list['Category']] = relationship(back_populates='base_category', cascade='all, delete', lazy='selectin')
    budget: Mapped['Budget | None'] = relationship(back_populates='categories', lazy='selectin')
    transactions: Mapped[list['Transaction']] = relationship(back_populates='category', lazy='selectin')

    name: Mapped[str] = mapped_column(index=True)
    type: Mapped[CategoryType]
