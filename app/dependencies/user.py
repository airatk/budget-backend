from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.utilities.exceptions.auth import UserUnauthorised
from app.utilities.security.jwt import decode_access_token
from core.databases.models import User
from core.databases.services import UserService


def identify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: Session = Depends(define_postgres_session),
) -> User:
    (user_id, error_message) = decode_access_token(credentials.credentials)

    if error_message:
        raise UserUnauthorised(message=error_message)

    user_service: UserService = UserService(session=session)
    user: User | None = user_service.get_by_id(user_id)

    if user is None:
        raise UserUnauthorised(message='The user does not seem to exist')

    return user
