from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.transaction import (
    TransactionCreationData,
    TransactionOutputData,
    TransactionsPeriodData,
    TransactionUpdateData,
)
from app.utilities.exceptions.records import (
    CouldNotAccessRecord,
    CouldNotFindRecord,
)
from core.databases.models import Account, Category, Transaction, User
from core.databases.repositories import TransactionRepository


transaction_router: APIRouter = APIRouter(prefix='/transaction', tags=['transaction'])


@transaction_router.get('/periods', response_model=list[TransactionsPeriodData])
async def get_periods(
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[TransactionsPeriodData]:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)
    periods_entities: list[tuple[int, int]] = await transaction_repository.get_user_transaction_periods(current_user)

    return [TransactionsPeriodData(year=year, month=month) for (year, month) in periods_entities]

@transaction_router.get('/list', response_model=list[TransactionOutputData])
async def get_transactions(
    transactions_period: TransactionsPeriodData = Depends(),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[Transaction]:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)

    return await transaction_repository.get_list(
        Transaction.account.has(user=current_user),
        func.DATE_PART('YEAR', Transaction.due_date) == transactions_period.year,
        func.DATE_PART('MONTH', Transaction.due_date) == transactions_period.month,
    )

@transaction_router.get('/item', response_model=TransactionOutputData)
async def get_transaction(
    transaction_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Transaction:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)
    transaction: Transaction | None = await transaction_repository.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    return transaction

@transaction_router.post('/create', response_model=TransactionOutputData, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreationData,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Transaction:
    if not any(transaction_data.account_id == account.id for account in current_user.accounts):
        raise CouldNotFindRecord(transaction_data.account_id, Account)

    if not any(transaction_data.category_id == category.id for category in current_user.categories):
        raise CouldNotFindRecord(transaction_data.category_id, Category)

    transaction_repository: TransactionRepository = TransactionRepository(session=session)

    return await transaction_repository.create(
        record_data=transaction_data.dict(),
    )

@transaction_router.patch('/update', response_model=TransactionOutputData)
async def update_transaction(
    transaction_data: TransactionUpdateData,
    transaction_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> Transaction:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)
    transaction: Transaction | None = await transaction_repository.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    return await transaction_repository.update(
        record=transaction,
        record_data=transaction_data.dict(),
    )

@transaction_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: PositiveInt = Query(..., alias='id'),
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> None:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)
    transaction: Transaction | None = await transaction_repository.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    await transaction_repository.delete(transaction)
