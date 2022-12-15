from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.schemas.authentication import (
    AuthenticationData,
    SignInCredentialsData,
)
from app.services import UserService
from app.utilities.security import create_token
from models import User


authentication_controller: APIRouter = APIRouter(tags=["authentication"])


@authentication_controller.post("/sign-in", response_model=AuthenticationData)
async def sign_in(
    credentials: SignInCredentialsData,
    session: Session = Depends(define_postgres_session),
):
    user_service: UserService = UserService(session=session)

    user: User | None = user_service.get_or_none_by_credentials(
        username=credentials.username,
        password=credentials.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided creditials are wrong",
        )

    user_access_token: str = create_token(user_id=user.id)

    return AuthenticationData(access_token=user_access_token)
