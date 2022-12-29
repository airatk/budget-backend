from fastapi import status

from .response import BaseApiException


class UserUnauthorised(BaseApiException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
        )


class WrongUsername(BaseApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="User with provided username was not found",
        )

class WrongPassword(BaseApiException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Provided password for {username} is wrong".format(
                username=username,
            ),
        )
