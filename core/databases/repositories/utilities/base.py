from typing import Any, Awaitable, Generic, Type, TypeVar

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement

from core.databases.models.utilities.base import BaseModel


Model = TypeVar('Model', bound=BaseModel)


class SingletonRepositoryMeta(type):
    _instances: dict['SingletonRepositoryMeta', type] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> type:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class BaseRepository(Generic[Model], metaclass=SingletonRepositoryMeta):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_list(self, *conditions: ColumnElement[bool]) -> list[Model]:
        query_result: Result[tuple[Model]] = await self.session.execute(
            select(self.model).where(*conditions),
        )

        return list(query_result.unique().scalars().all())

    async def get(self, *conditions: ColumnElement[bool]) -> Model | None:
        query_result: Result[tuple[Model]] = await self.session.execute(
            select(self.model).where(*conditions),
        )

        return query_result.unique().scalars().one_or_none()

    async def get_by_id(self, record_id: int) -> Model | None:
        return await self.session.get(self.model, record_id)

    async def create(self, record_data: dict[str, Any], **additional_attributes: Any) -> Model:
        record_data |= additional_attributes

        record: Model = self.model(**record_data)

        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)

        return record

    async def update(self, record: Model, record_data: dict[str, Any], **additional_attributes: Any) -> Model:
        record_data |= additional_attributes

        for field_key, field_value in record_data.items():
            setattr(record, field_key, await field_value if isinstance(field_value, Awaitable) else field_value)

        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)

        return record

    async def delete(self, record: Model) -> None:
        await self.session.delete(record)
        await self.session.commit()
