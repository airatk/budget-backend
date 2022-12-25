from typing import Any, TypeAlias

from fastapi import HTTPException
from pydantic import BaseModel


ErrorData: TypeAlias = dict[str, Any]

class ErrorResponseData(BaseModel):
    message: str
    error_data: ErrorData | None


class BaseApiException(HTTPException):
    def __init__(self, status_code: int, message: str, error_data: ErrorData | None = None) -> None:
        super().__init__(
            status_code=status_code,
            detail=ErrorResponseData(
                message=message,
                error_data=error_data,
            ).dict(
                exclude_none=True,
            ),
        )
