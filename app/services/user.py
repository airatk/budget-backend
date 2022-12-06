from sqlalchemy.orm import Session

from models import User

from .utilities.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=User,
            session=session
        )
