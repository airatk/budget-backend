from sqlalchemy.orm import Session

from models import Category

from .utilities.base import BaseService


class CategoryService(BaseService[Category]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Category,
            session=session,
        )
