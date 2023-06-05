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

    user: Mapped['User'] = relationship('User', back_populates='categories', lazy='joined')
    base_category: Mapped['Category | None'] = relationship('Category', back_populates='subcategories', lazy='joined', remote_side=lambda: Category.id)
    subcategories: Mapped[list['Category']] = relationship('Category', back_populates='base_category', cascade='all, delete', lazy='joined')
    budget: Mapped['Budget | None'] = relationship('Budget', back_populates='categories', lazy='joined')
    transactions: Mapped[list['Transaction']] = relationship('Transaction', back_populates='category', lazy='joined')

    name: Mapped[str] = mapped_column(index=True)
    type: Mapped[CategoryType]
