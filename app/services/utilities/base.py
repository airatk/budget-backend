from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Boolean, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import ColumnElement

from app.schemas.utilities.base import BaseData, BaseUpdateData
from models.utilities.base import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class BaseService(Generic[Model]):
    def __init__(self, model_class: Type[Model], session: Session):
        self.model_class = model_class
        self.session = session

    def get_or_none(self, *conditions: ColumnElement[Boolean]) -> Model | None:
        query: Any = select(self.model_class).where(*conditions)

        return self.session.scalar(query)

    def get(self, *conditions: ColumnElement[Boolean]) -> Model:
        record: Model | None = self.get_or_none(*conditions)

        if record is None:
            raise NotImplementedError

        return record

    def get_by_id(self, record_id: int, *additional_conditions: ColumnElement[Boolean]) -> Model:
        return self.get(
            self.model_class.id == record_id,
            *additional_conditions,
        )

    def get_list(self, *conditions) -> list[Model]:
        query: Any = select(self.model_class).where(*conditions)

        return self.session.scalars(query).all()

    def create(self, record_data: BaseData, **additional_attributes: Any) -> Model:
        record: Model = self.model_class(
            **record_data.dict(),
            **additional_attributes,
        )

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def update(self, record_id: int, record_data: BaseUpdateData, *additional_conditions: ColumnElement[Boolean]) -> Model:
        record: Model = self.get_by_id(record_id, *additional_conditions)

        for (field, datum) in record_data.dict().items():
            setattr(record, field, datum)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def delete(self, record_id: int, *additional_conditions: ColumnElement[Boolean]):
        record: Model = self.get_by_id(record_id, *additional_conditions)

        self.session.delete(record)
        self.session.commit()
