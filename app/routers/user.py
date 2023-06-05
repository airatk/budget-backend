from fastapi import APIRouter, Depends, Query
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.user import UserOutputData
from app.utilities.exceptions.records import (
    CouldNotAccessRecord,
    CouldNotFindRecord,
)
from app.utilities.exceptions.users import SelfIsNotRelative
from core.databases.models import User
from core.databases.repositories import UserRepository


user_router: APIRouter = APIRouter(prefix='/user', tags=['user'])


@user_router.get('/current', response_model=UserOutputData)
async def get_current_user(
    current_user: User = Depends(identify_user),
) -> User:
    return current_user

@user_router.get('/relative', response_model=UserOutputData)
async def get_relative(
    relative_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> User:
    if relative_id == current_user.id:
        raise SelfIsNotRelative()

    user_repository: UserRepository = UserRepository(session=session)
    user: User | None = await user_repository.get_by_id(relative_id)

    if user is None:
        raise CouldNotFindRecord(relative_id, User)

    if user.family != current_user.family:
        raise CouldNotAccessRecord(relative_id, User)

    return user
