from re import sub

from sqlalchemy import BigInteger, Column, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class BaseModel:
    __name__: str
    metadata: MetaData

    id: int = Column(BigInteger, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        pre_snake_case_name: str = sub("([A-Z]+)", r" \1", cls.__name__)
        pre_snake_case_name = sub("([A-Z][a-z]+)", r" \1", pre_snake_case_name)

        return "_".join(pre_snake_case_name.lower().split())

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(id={0.id})".format(self)
