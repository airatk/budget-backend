from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.services import UserService
from app.utilities.security import decode_token
from models import User


def identify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: Session = Depends(define_postgres_session),
) -> User:
    (user_id, error_message) = decode_token(credentials.credentials)

    if error_message is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_message,
        )

    user_service: UserService = UserService(session=session)

    user: User | None = user_service.get_or_none_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user does not seem to exist",
        )

    return user
