from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel


if TYPE_CHECKING:
    from .user import User


class Family(BaseModel):
    members: "User" = relationship("User", back_populates="family")

    access_code: str = Column(String(8), unique=True, nullable=False)

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id})".format(self)
