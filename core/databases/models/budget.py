from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel
from .utilities.types import BudgetType


if TYPE_CHECKING:
    from .category import Category
    from .user import User


class Budget(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship('User', back_populates='budgets', lazy='joined')
    categories: Mapped[list['Category']] = relationship('Category', back_populates='budget', lazy='joined')

    name: Mapped[str] = mapped_column(index=True)
    type: Mapped[BudgetType]
    planned_outcomes: Mapped[float] = mapped_column(default=0)
