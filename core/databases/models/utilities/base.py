from enum import StrEnum
from re import sub
from typing import Any

from sqlalchemy import BigInteger, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class BaseModel(AsyncAttrs, DeclarativeBase):
    type_annotation_map: dict[type, Any] = {
        int: BigInteger,
        StrEnum: Enum(StrEnum, values_callable=lambda enum: [enum_field.value for enum_field in enum]),
    }

    @declared_attr.directive
    def __tablename__(cls) -> str:
        pre_snake_case_name: str = sub('([A-Z]+)', r' \1', cls.__name__)
        pre_snake_case_name = sub('([A-Z][a-z]+)', r' \1', pre_snake_case_name)

        return '_'.join(pre_snake_case_name.lower().split())

    def __repr__(self) -> str:
        return '{0.__class__.__name__}(id={0.id})'.format(self)

    id: Mapped[int] = mapped_column(primary_key=True)
