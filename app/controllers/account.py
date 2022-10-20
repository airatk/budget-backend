from typing import Literal

from sqlalchemy.orm import Session

from pydantic import BaseModel
from pydantic import Field

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.models import User
from app.models import Account


account_controller: APIRouter = APIRouter(prefix="/account")


class AccountData(BaseModel):
    id: int | None
    name: str = Field(min_length=1)
    currency: Literal[ "RUB", "USD" ]
    openning_balance: float = 0.00


@account_controller.post("/create")
async def create_account(account_data: AccountData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account = Account(
        user=current_user,
        name=account_data.name,
        currency=account_data.currency,
        openning_balance=account_data.openning_balance
    )

    session.add(account)
    session.commit()

    return {
        "message": "Account was created"
    }

@account_controller.put("/update")
async def update_account(account_data: AccountData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account | None = session.query(Account).filter(
        Account.id == account_data.id,
        Account.id.in_(account.id for account in current_user.accounts)
    ).one_or_none()

    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No account with given `id` was found")

    account.name = account_data.name
    account.currency = account_data.currency
    account.openning_balance = account_data.openning_balance

    session.commit()

    return {
        "message": "Account was updated"
    }

@account_controller.delete("/delete")
async def delete_account(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account | None = session.query(Account).filter(
        Account.id == id,
        Account.id.in_(account.id for account in current_user.accounts)
    ).one_or_none()

    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No account with given `id` was found")

    session.delete(account)
    session.commit()

    return {
        "message": "Account was deleted"
    }
