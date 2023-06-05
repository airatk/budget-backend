from typing import Annotated

from pydantic import Field


MIN_TRANSACTION_YEAR: int = 2000
MIN_TRANSACTION_MONTH: int = 1
MAX_TRANSACTION_MONTH: int = 12


Year = Annotated[
    int,
    Field(..., ge=MIN_TRANSACTION_YEAR),
]
Month = Annotated[
    int,
    Field(..., ge=MIN_TRANSACTION_MONTH, le=MAX_TRANSACTION_MONTH),
]
