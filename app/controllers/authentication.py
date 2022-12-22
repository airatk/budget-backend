from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.schemas.authentication import AuthenticationData
from app.services import UserService
from core.security import create_token
from models import User


authentication_controller: APIRouter = APIRouter(tags=["authentication"])


@authentication_controller.get("/sign-in", response_model=AuthenticationData)
async def sign_in(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    session: Session = Depends(define_postgres_session),
):
    user_service: UserService = UserService(session=session)

    user: User | None = user_service.get_or_none_by_credentials(
        username=credentials.username,
        password=credentials.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provided creditials are wrong",
        )

    user_access_token: str = create_token(user_id=user.id)

    return AuthenticationData(access_token=user_access_token)
