from .utilities.base import BaseData
from .utilities.types import NonEmptyStr


class SignInCredentialsData(BaseData, anystr_strip_whitespace=True):
    username: NonEmptyStr
    password: NonEmptyStr

class AuthenticationData(BaseData, anystr_strip_whitespace=True):
    access_token: NonEmptyStr
