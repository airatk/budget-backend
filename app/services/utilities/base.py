from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.utilities.base import BaseData, BaseUpdateData
from models.utilities.base import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class BaseService(Generic[Model]):
    def __init__(self, model_class: Type[Model], session: Session):
        self.model_class = model_class
        self.session = session

    def get_one_or_none(self, id: int, *additional_conditions: bool) -> Model | None:
        query: Any = select(self.model_class).where(
            self.model_class.id == id,
            *additional_conditions
        )

        return self.session.scalar(query)

    def get_one(self, id: int, *additional_conditions: bool) -> Model:
        record: Model | None = self.get_one_or_none(id, *additional_conditions)

        if record is None:
            raise NotImplementedError

        return record

    def create(self, record_data: BaseData, **additional_attributes: Any) -> Model:
        record: Model = self.model_class(
            **record_data.dict(),
            **additional_attributes
        )

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def update(self, record_data: BaseUpdateData, *additional_conditions: bool) -> Model:
        record: Model = self.get_one(
            record_data.id,
            *additional_conditions
        )

        for (field, value) in record_data.dict().items():
            setattr(record, field, value)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def delete(self, id: int, *additional_conditions: bool):
        record: Model = self.get_one(id, *additional_conditions)

        self.session.delete(record)
        self.session.commit()
