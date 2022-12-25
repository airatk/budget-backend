from typing import cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from models import Transaction, User

from .utilities.base import BaseService


class TransactionService(BaseService[Transaction]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Transaction,
            session=session,
        )

    def get_transaction_periods_of_user(self, user: User) -> list[tuple[int, int]]:
        query: Select = select(
            func.DATE_PART("YEAR", Transaction.due_date),
            func.DATE_PART("MONTH", Transaction.due_date),
        ).where(
            Transaction.account.has(user=user),
        )

        return cast(
            list[tuple[int, int]],
            self.session.execute(query).unique().all(),
        )
