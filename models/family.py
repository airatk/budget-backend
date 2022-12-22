from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel


if TYPE_CHECKING:
    from .budget import Budget
    from .user import User


class Family(BaseModel):
    members: "User" = relationship("User", back_populates="family")
    budgets: "Budget" = relationship("Budget", back_populates="family", passive_deletes=True)

    access_code: str = Column(String(8), unique=True, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id})".format(self)
