from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from app.dependencies.session import define_local_session

from app.schemas.authentication import SignInCredentials
from app.schemas.authentication import AuthenticationData

from app.models import User

from app.utilities.security import create_token


authentication_controller: APIRouter = APIRouter()


@authentication_controller.post("/sign-in", response_model=AuthenticationData)
async def sign_in(credentials: SignInCredentials, session: Session = Depends(define_local_session)):
    user: User = session.query(User).\
        filter(
            User.username == credentials.username,
            User.password == credentials.password
        ).\
        one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided creditials are wrong"
        )

    return AuthenticationData(access_token=create_token(user_id=user.id))
