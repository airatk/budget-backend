from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.user import identify_user
from app.schemas.family import FamilyOutputData
from models import User


family_controller: APIRouter = APIRouter(prefix="/family", tags=["family"])


@family_controller.get("/current", response_model=FamilyOutputData)
async def get_family(
    current_user: User = Depends(identify_user),
):
    if current_user.family is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any family",
        )

    return current_user.family
