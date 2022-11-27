from typing import Any

from pydantic import BaseModel


class BaseUpdateModel(BaseModel):
    def dict(self, **keyword_arguments) -> dict[str, Any]:
        keyword_arguments["exclude_unset"] = True

        return super().dict(**keyword_arguments)
