from .user import UserOutputData
from .utilities.base import BaseData


class AuthenticationData(BaseData):
    access_token: str
    user: UserOutputData
