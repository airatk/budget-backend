from sqlalchemy.orm import Session

from models import Transaction

from .utilities.base import BaseService


class TransactionService(BaseService[Transaction]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Transaction,
            session=session,
        )
