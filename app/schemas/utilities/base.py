from typing import Any

from pydantic import BaseModel


class BaseData(BaseModel):
    ...  # noqa: WPS428, WPS604


class BaseUpdateData(BaseModel):
    def dict(self, **keyword_arguments) -> dict[str, Any]:
        keyword_arguments["exclude_unset"] = True

        return super().dict(**keyword_arguments)
