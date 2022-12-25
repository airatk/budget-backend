from sqlalchemy.orm import Session

from models import User

from .utilities.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=User,
            session=session,
        )

    def get_by_credentials(self, username: str, password: str) -> User | None:
        return self.get(
            User.username == username,
            User.password == password,
        )
