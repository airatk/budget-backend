from sqlalchemy.orm import Session

from pydantic import PositiveInt

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from models import User

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user

from app.schemas.user import UserData


users_controller: APIRouter = APIRouter(prefix="/users")


@users_controller.get("/current", response_model=UserData)
async def get_current_user(
    current_user: User = Depends(identify_user)
):
    return current_user

@users_controller.get("/relative", response_model=UserData)
async def get_relative(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    user: User | None = session.query(User).\
        filter(
            User.id == id,
            User.family == current_user.family
        ).\
        one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a relative with given `id`"
        )

    return user
