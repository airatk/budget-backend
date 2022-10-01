from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status
from fastapi import Security
from fastapi.security import APIKeyHeader

from app.models import User

from app.utilities.security import decode_token
from app.utilities.database import engine


async def identify_user(token: str = Security(APIKeyHeader(name="UserAccessToken"))) -> User:
    (user_id, error_message) = decode_token(token)

    if error_message is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

    with Session(bind=engine) as session:
        user: User = session.query(User).filter(User.id == user_id).one()

    return user
