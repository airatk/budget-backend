from sqlalchemy.orm import Session

from core.databases.models import Account

from .utilities.base import BaseService


class AccountService(BaseService[Account]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Account,
            session=session,
        )
