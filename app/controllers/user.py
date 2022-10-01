from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


user_controller: APIRouter = APIRouter(prefix="/user")


@user_controller.get("/current")
async def get_current_user(current_user: User = Depends(identify_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }
