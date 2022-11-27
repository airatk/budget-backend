from pydantic import BaseModel

from .utilities.types import NonEmptyStr


class SignInCredentialsData(BaseModel, anystr_strip_whitespace=True):
    username: NonEmptyStr
    password: NonEmptyStr

class AuthenticationData(BaseModel, anystr_strip_whitespace=True):
    access_token: NonEmptyStr
