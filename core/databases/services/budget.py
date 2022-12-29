from sqlalchemy.orm import Session

from core.databases.models import Budget

from .utilities.base import BaseService


class BudgetService(BaseService[Budget]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Budget,
            session=session,
        )
