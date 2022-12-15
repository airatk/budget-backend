from fastapi import APIRouter, Depends, Query
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
    relative_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    user_service: UserService = UserService(session=session)

    return user_service.get_relative_by_id(
        relative_id=relative_id,
        user=current_user,
    )
