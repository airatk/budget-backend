from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel
from .utilities.constants import MAX_USERNAME_LENGTH


if TYPE_CHECKING:
    from .account import Account
    from .budget import Budget
    from .category import Category
    from .family import Family


class User(BaseModel):
    family_id: int = Column(BigInteger, ForeignKey('family.id', ondelete='SET NULL'))

    family: 'Family' = relationship('Family', back_populates='members')
    accounts: list['Account'] = relationship('Account', back_populates='user', passive_deletes=True)
    categories: list['Category'] = relationship('Category', back_populates='user', passive_deletes=True)
    budgets: list['Budget'] = relationship('Budget', back_populates='user', passive_deletes=True)

    username: str = Column(String(MAX_USERNAME_LENGTH), unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
