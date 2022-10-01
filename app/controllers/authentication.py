from sqlalchemy.orm import Session

from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.models import User

from app.utilities.database import engine
from app.utilities.security import create_token


authentication_controller: APIRouter = APIRouter()


class SignInCredentials(BaseModel):
    username: str
    password: str


@authentication_controller.post("/sign-in")
async def sign_in(credentials: SignInCredentials):
    with Session(bind=engine) as session:
        user: User = session.query(User).filter(
            User.username == credentials.username,
            User.password == credentials.password
        ).one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provided creditials are wrong")

    return {
        "access_token": create_token(user_id=user.id)
    }
