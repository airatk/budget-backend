from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.services import UserService
from app.utilities.exceptions import UserUnauthorised
from core.security import decode_token
from models import User


def identify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: Session = Depends(define_postgres_session),
) -> User:
    (user_id, error_message) = decode_token(credentials.credentials)

    if error_message:
        raise UserUnauthorised(message=error_message)

    user_service: UserService = UserService(session=session)
    user: User | None = user_service.get_by_id(user_id)

    if user is None:
        raise UserUnauthorised(message="The user does not seem to exist")

    return user
