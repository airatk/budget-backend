from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status
from fastapi import Security
from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.dependencies.session import define_local_session

from app.models import User

from app.utilities.security import decode_token


async def identify_user(token: str = Security(APIKeyHeader(name="UserAccessToken")), session: Session = Depends(define_local_session)) -> User:
    (user_id, error_message) = decode_token(token)

    if error_message is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    user: User | None = session.query(User).\
        filter(User.id == user_id).\
        one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user does not seem to exist"
        )

    return user
