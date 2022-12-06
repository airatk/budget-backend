from sqlalchemy.orm import Session

from models import Family

from .utilities.base import BaseService


class FamilyService(BaseService[Family]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Family,
            session=session
        )
