from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from app.utilities.exceptions.auth import UserUnauthorised
from app.utilities.security.jwt import decode_access_token
from core.databases.models import User
from core.databases.repositories import UserRepository


async def identify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: AsyncSession = Depends(define_postgres_session),
) -> User:
    (user_id, error_message) = decode_access_token(credentials.credentials)

    if not user_id:
        raise UserUnauthorised(message=error_message)

    user_repository: UserRepository = UserRepository(session=session)
    user: User | None = await user_repository.get_by_id(user_id)

    if user is None:
        raise UserUnauthorised(message='The user does not seem to exist')

    return user
