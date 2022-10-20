from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.user import identify_user

from app.models import User


user_controller: APIRouter = APIRouter(prefix="/user")


class CurrentUser(BaseModel):
    id: int
    family_id: int | None
    username: str

    class Config:
        orm_mode = True


@user_controller.get("/current", response_model=CurrentUser)
async def get_current_user(current_user: User = Depends(identify_user)):
    return CurrentUser.from_orm(obj=current_user)


@user_controller.get("/summary")
async def get_summary(current_user: User = Depends(identify_user)):
    # TODO: There should be summary for current period & all the time.
    #       It should include `Balance`, `Income` & `Outcome` only.

    pass

@user_controller.get("/last-7-days")
async def get_last_7_days_highlight(current_user: User = Depends(identify_user)):
    pass

@user_controller.get("/monthly-trend")
async def get_monthly_trend(current_user: User = Depends(identify_user)):
    pass

@user_controller.get("/balances")
async def get_balances(current_user: User = Depends(identify_user)):
    pass

@user_controller.get("/accounts")
async def get_accounts(current_user: User = Depends(identify_user)):
    return current_user.accounts
