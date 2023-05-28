from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .utilities.base import BaseModel


if TYPE_CHECKING:
    from .user import User


class Family(BaseModel):
    members: list['User'] = relationship('User', back_populates='family')

    access_code: str = Column(String, unique=True, nullable=False)
