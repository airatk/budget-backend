from pydantic import BaseModel


class SignInCredentials(BaseModel):
    username: str
    password: str

class AuthenticationData(BaseModel):
    access_token: str
