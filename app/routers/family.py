from fastapi import APIRouter, Depends

from app.dependencies.user import identify_user
from app.schemas.family import FamilyOutputData
from app.utilities.exceptions.users import NotFamilyMember
from core.databases.models import Family, User


family_router: APIRouter = APIRouter(prefix='/family', tags=['family'])


@family_router.get('/current', response_model=FamilyOutputData)
async def get_family(
    current_user: User = Depends(identify_user),
) -> Family:
    if current_user.family is None:
        raise NotFamilyMember()

    return current_user.family
