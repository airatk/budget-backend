from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .utilities.base import BaseModel


if TYPE_CHECKING:
    from .user import User


class Family(BaseModel):
    members: Mapped[list['User']] = relationship('User', back_populates='family', lazy='joined')

    access_code: Mapped[str] = mapped_column(unique=True)
