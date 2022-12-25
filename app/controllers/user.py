from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.user import UserData
from app.services import UserService
from models import User


user_controller: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_controller.get("/current", response_model=UserData)
async def get_current_user(
    current_user: User = Depends(identify_user),
):
    return current_user

@user_controller.get("/relative", response_model=UserData)
async def get_relative(
    relative_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    user_service: UserService = UserService(session=session)

    user: User | None = user_service.get_by_id(relative_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if user.family != current_user.family:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return user
