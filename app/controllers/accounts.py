from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.schemas.account import AccountData
from app.schemas.account import AccountBalance
from app.schemas.account import AccountsSummary
from app.schemas.account import DailyOutcomes

from app.models import User
from app.models import Account
from app.models.transaction import TransactionType


accounts_controller: APIRouter = APIRouter(prefix="/accounts")


@accounts_controller.get("/summary", response_model=AccountsSummary)
async def get_summary(current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    # TODO: There should be summary for current period & all the time.
    #       It should include `Balance`, `Income` & `Outcome` only.
    pass

@accounts_controller.get("/last-n-days", response_model=list[DailyOutcomes])
async def get_last_n_days_highlight(n_days: int = 7, current_user: User = Depends(identify_user)):
    pass

@accounts_controller.get("/monthly-trend")
async def get_monthly_trend(current_user: User = Depends(identify_user)):
    pass

@accounts_controller.get("/balances", response_model=list[AccountBalance])
async def get_balances(current_user: User = Depends(identify_user)):
    balances: list[AccountBalance] = []

    for account in current_user.accounts:
        account_incomes: float = sum(
            transaction.amount for transaction in account.transactions
            if transaction.type == TransactionType.INCOME
        )
        account_outcomes: float = sum(
            transaction.amount for transaction in account.transactions
            if transaction.type == TransactionType.OUTCOME
        )

        account_balance: AccountBalance = AccountBalance(
            account=account.name,
            balance=(account.openning_balance + account_incomes) - account_outcomes
        )

        balances.append(account_balance)
    
    return balances

@accounts_controller.get("/list", response_model=list[AccountData])
async def get_accounts(current_user: User = Depends(identify_user)):
    return [ AccountData.from_orm(obj=account) for account in current_user.accounts ]

@accounts_controller.post("/create", response_model=str)
async def create_account(account_data: AccountData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account = Account(
        user=current_user,
        name=account_data.name,
        currency=account_data.currency,
        openning_balance=account_data.openning_balance
    )

    session.add(account)
    session.commit()

    return "Account was created"

@accounts_controller.put("/update", response_model=str)
async def update_account(account_data: AccountData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account | None = session.query(Account).\
        filter(
            Account.id == account_data.id,
            Account.user == current_user
        ).\
        one_or_none()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have an account with given `id`"
        )

    account.name = account_data.name
    account.currency = account_data.currency
    account.openning_balance = account_data.openning_balance

    session.commit()

    return "Account was updated"

@accounts_controller.delete("/delete", response_model=str)
async def delete_account(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    account: Account | None = session.query(Account).\
        filter(
            Account.id == id,
            Account.user == current_user
        ).\
        one_or_none()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have an account with given `id`"
        )

    session.delete(account)
    session.commit()

    return "Account was deleted"
