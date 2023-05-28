from typing import Any

from pydantic import BaseModel


class BaseData(BaseModel):
    """Base class for data of input & output."""


class BaseUpdateData(BaseData):
    def dict(self, **keyword_arguments: Any) -> dict[str, Any]:
        keyword_arguments['exclude_unset'] = True

        return super().dict(**keyword_arguments)
