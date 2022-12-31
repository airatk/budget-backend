from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.schemas.authentication import AuthenticationData
from app.utilities.exceptions.auth import WrongPassword, WrongUsername
from app.utilities.security.jwt import create_access_token
from core.databases.models import User
from core.databases.services import UserService


authentication_controller: APIRouter = APIRouter(tags=["authentication"])


@authentication_controller.get("/sign-in", response_model=AuthenticationData)
async def sign_in(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    session: Session = Depends(define_postgres_session),
) -> AuthenticationData:
    user_service: UserService = UserService(session=session)
    user: User | None = user_service.get_by_username(credentials.username)

    if user is None:
        raise WrongUsername()

    if user.password != credentials.password:
        raise WrongPassword(username=user.username)

    return AuthenticationData(
        access_token=create_access_token(user_id=user.id),
    )
