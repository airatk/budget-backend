from typing import Annotated

from pydantic import Field

from app.utilities.constants import (
    MAX_TRANSACTION_MONTH,
    MIN_TRANSACTION_MONTH,
    MIN_TRANSACTION_YEAR,
)


Year = Annotated[
    int,
    Field(..., ge=MIN_TRANSACTION_YEAR),
]
Month = Annotated[
    int,
    Field(..., ge=MIN_TRANSACTION_MONTH, le=MAX_TRANSACTION_MONTH),
]
