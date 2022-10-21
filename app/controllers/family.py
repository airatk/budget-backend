from string import ascii_lowercase

from random import choices

from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.schemas.family import FamilyData

from app.models import User
from app.models import Family


family_controller: APIRouter = APIRouter(prefix="/family")


@family_controller.get("/join", response_model=FamilyData)
async def join_family(access_code: str, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    family: Family | None = session.query(Family).\
        filter(Family.access_code == access_code).\
        one_or_none()
    
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no family with given `access_code`"
        )
    
    current_user.family = family

    session.commit()

    return FamilyData.from_orm(obj=family)

@family_controller.get("/current", response_model=FamilyData)
async def get_family(current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    if current_user.family is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any family"
        )

    return FamilyData.from_orm(obj=current_user.family)

@family_controller.post("/create", response_model=str)
async def create_family(current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    if current_user.family is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of a family"
        )

    access_code: str = "".join(choices(ascii_lowercase, k=8))

    family: Family = Family(
        access_code=access_code,
        members=[ current_user ]
    )

    session.add(family)
    session.commit()

    return "Family was created"

@family_controller.put("/update", response_model=str)
async def update_family(family_data: FamilyData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    if current_user.family is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any family"
        )

    current_user.family.access_code = family_data.access_code

    session.commit()

    return "Family was updated"

@family_controller.delete("/delete", response_model=str)
async def delete_family(current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    if current_user.family is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any family"
        )
    
    session.delete(current_user.family)
    session.commit()

    return "Family was deleted"
