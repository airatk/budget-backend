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

    def get_list(self, *conditions) -> list[Model]:
        query: Any = select(self.model_class).where(*conditions)

        return self.session.scalars(query).all()

    def get(self, *conditions: ColumnElement[Boolean]) -> Model | None:
        query: Any = select(self.model_class).where(*conditions)

        return self.session.scalar(query)

    def get_by_id(self, record_id: int) -> Model | None:
        return self.get(
            self.model_class.id == record_id,
        )

    def create(self, record_data: BaseData, **additional_attributes: Any) -> Model:
        record_data_dict: dict[str, Any] = record_data.dict() | additional_attributes
        record: Model = self.model_class(**record_data_dict)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def update(self, record: Model, record_data: BaseUpdateData, **additional_attributes: Any) -> Model:
        record_data_dict: dict[str, Any] = record_data.dict() | additional_attributes

        for (field, datum) in record_data_dict.items():
            setattr(record, field, datum)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def delete(self, record: Model):
        self.session.delete(record)
        self.session.commit()
