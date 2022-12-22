from sqlalchemy.orm import Session

from models import User

from .utilities.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=User,
            session=session,
        )

    def get_or_none_by_credentials(self, username: str, password: str) -> User | None:
        return self.get_or_none(
            User.username == username,
            User.password == password,
        )

    def get_or_none_by_id(self, user_id: int) -> User | None:
        return self.get_or_none(
            User.id == user_id,
        )

    def get_relative_by_id(self, relative_id: int, user: User) -> User:
        return self.get_by_id(
            relative_id,
            User.family == user.family,
        )
