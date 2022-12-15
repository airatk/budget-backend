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
from app.services import AccountService
from models import Account, User
from models.utilities.types import TransactionType


account_controller: APIRouter = APIRouter(prefix="/account", tags=["account"])


@account_controller.get("/balances", response_model=list[AccountBalanceData])
async def get_balances(
    current_user: User = Depends(identify_user),
):
    balances: list[AccountBalanceData] = []

    for account in current_user.accounts:
        account_incomes: float = sum(
            transaction.amount for transaction in account.transactions if transaction.type == TransactionType.INCOME
        )
        account_outcomes: float = sum(
            transaction.amount for transaction in account.transactions if transaction.type == TransactionType.OUTCOME
        )
        account_balance: AccountBalanceData = AccountBalanceData(
            account=account.name,
            balance=account.openning_balance + account_incomes - account_outcomes,
        )

        balances.append(account_balance)

    return balances

@account_controller.get("/list", response_model=list[AccountOutputData])
async def get_accounts(
    current_user: User = Depends(identify_user),
):
    return current_user.accounts

@account_controller.post("/create", response_model=AccountOutputData, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    account_service: AccountService = AccountService(session=session)

    return account_service.create(
        record_data=account_data,
        user=current_user,
    )

@account_controller.patch("/update", response_model=AccountOutputData)
async def update_account(
    account_data: AccountUpdateData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    account_service: AccountService = AccountService(session=session)

    return account_service.update(
        account_data,
        Account.user == current_user,
    )

@account_controller.delete("/delete", response_model=str)
async def delete_account(
    account_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    account_service: AccountService = AccountService(session=session)

    account_service.delete(
        account_id,
        Account.user == current_user,
    )

    return "Account was deleted"
