from pydantic import Field

from .utilities.base import BaseData


class AuthenticationData(BaseData):
    access_token: str = Field(..., min_length=1)
