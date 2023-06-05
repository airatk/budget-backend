from fastapi import status

from .response import BaseApiException


class UserUnauthorised(BaseApiException):
    def __init__(self, message: str | None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message or 'User is not authorised',
        )


class UsernameAlreadyExists(BaseApiException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='User {0} already exists'.format(username),
            error_data={
                'username': username,
            },
        )

class WrongUsername(BaseApiException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message='User {0} does not exist'.format(username),
            error_data={
                'username': username,
            },
        )

class WrongPassword(BaseApiException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message='Provided password for {0} is wrong'.format(username),
            error_data={
                'username': username,
            },
        )
