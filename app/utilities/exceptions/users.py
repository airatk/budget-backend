from fastapi import status

from .response import BaseApiException


class SelfIsNotRelative(BaseApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Provided `id` belongs to the user himself",
        )

class NotFamilyMember(BaseApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="The user is not a member of any family",
        )
