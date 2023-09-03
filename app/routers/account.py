from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

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
from core.databases.repositories import AccountRepository


account_router: APIRouter = APIRouter(prefix='/account', tags=['account'])


@account_router.get('/balances', response_model=list[AccountBalanceData])
async def get_balances(
    current_user: User = Depends(identify_user),
) -> list[AccountBalanceData]:
    return [
        AccountBalanceData(
            account=account.name,
            balance=sum_transactions_of_given_type(
                transactions=account.transactions,
                transaction_type=TransactionType.INCOME,
                initial_amount=account.opening_balance,
            ) - sum_transactions_of_given_type(
                transactions=account.transactions,
                transaction_type=TransactionType.OUTCOME,
            ),
        )
        for account in current_user.accounts
    ]

@account_router.get('/list', response_model=list[AccountOutputData])
async def get_accounts(
    current_user: User = Depends(identify_user),
) -> list[Account]:
    return current_user.accounts

@account_router.post('/create', response_model=AccountOutputData, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreationData,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Account:
    account_repository: AccountRepository = AccountRepository(session=session)

    return await account_repository.create(
        record_data=account_data.dict(),
        user=current_user,
    )

@account_router.patch('/update', response_model=AccountOutputData)
async def update_account(
    account_data: AccountUpdateData,
    account_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Account:
    account_repository: AccountRepository = AccountRepository(session=session)
    account: Account | None = await account_repository.get_by_id(account_id)

    if account is None:
        raise CouldNotFindRecord(account_id, Account)

    if account.user != current_user:
        raise CouldNotAccessRecord(account_id, Account)

    return await account_repository.update(
        record=account,
        record_data=account_data.dict(),
    )

@account_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> None:
    account_repository: AccountRepository = AccountRepository(session=session)
    account: Account | None = await account_repository.get_by_id(account_id)

    if account is None:
        raise CouldNotFindRecord(account_id, Account)

    if account.user != current_user:
        raise CouldNotAccessRecord(account_id, Account)

    await account_repository.delete(account)
