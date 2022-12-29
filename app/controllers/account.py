from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.account import (
    AccountBalanceData,
    AccountCreationData,
    AccountOutputData,
    AccountUpdateData,
)
from app.utilities.callables import sum_transactions_of_given_type
from app.utilities.exceptions.records import (
    CouldNotAccessRecord,
    CouldNotFindRecord,
)
from core.databases.models import Account, User
from core.databases.models.utilities.types import TransactionType
from core.databases.services import AccountService


account_controller: APIRouter = APIRouter(prefix="/account", tags=["account"])


@account_controller.get("/balances", response_model=list[AccountBalanceData])
async def get_balances(
    current_user: User = Depends(identify_user),
) -> list[AccountBalanceData]:
    return [
        AccountBalanceData(
            account=account.name,
            balance=sum_transactions_of_given_type(
                transactions=account.transactions,
                transaction_type=TransactionType.INCOME,
                initial_amount=account.openning_balance,
            ) - sum_transactions_of_given_type(
                transactions=account.transactions,
                transaction_type=TransactionType.OUTCOME,
            ),
        ) for account in current_user.accounts
    ]

@account_controller.get("/list", response_model=list[AccountOutputData])
async def get_accounts(
    current_user: User = Depends(identify_user),
) -> list[Account]:
    return current_user.accounts

@account_controller.post("/create", response_model=AccountOutputData, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> Account:
    account_service: AccountService = AccountService(session=session)

    return account_service.create(
        record_data=account_data.dict(),
        user=current_user,
    )

@account_controller.patch("/update", response_model=AccountOutputData)
async def update_account(
    account_data: AccountUpdateData,
    account_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
) -> Account:
    account_service: AccountService = AccountService(session=session)
    account: Account | None = account_service.get_by_id(account_id)

    if account is None:
        raise CouldNotFindRecord(account_id, Account)

    if account.user != current_user:
        raise CouldNotAccessRecord(account_id, Account)

    return account_service.update(
        record=account,
        record_data=account_data.dict(),
    )

@account_controller.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    account_service: AccountService = AccountService(session=session)
    account: Account | None = account_service.get_by_id(account_id)

    if account is None:
        raise CouldNotFindRecord(account_id, Account)

    if account.user != current_user:
        raise CouldNotAccessRecord(account_id, Account)

    account_service.delete(account)
