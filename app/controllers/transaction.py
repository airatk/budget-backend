from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.transaction import (
    TransactionCreationData,
    TransactionOutputData,
    TransactionsPeriod,
    TransactionUpdateData,
)
from app.services import TransactionService
from app.utilities.exceptions import CouldNotAccessRecord, CouldNotFindRecord
from models import Transaction, User

from .utilities.constants import (
    TRANSACTION_MAXIMAL_MONTH,
    TRANSACTION_MINIMAL_MONTH,
    TRANSACTION_MINIMAL_YEAR,
)


transaction_controller: APIRouter = APIRouter(prefix="/transaction", tags=["transaction"])


@transaction_controller.get("/periods", response_model=list[TransactionsPeriod])
async def get_periods(
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)
    periods_entities: list[tuple[int, int]] = transaction_service.get_transaction_periods_of_user(current_user)

    return [TransactionsPeriod(year=period_entities[0], month=period_entities[1]) for period_entities in periods_entities]

@transaction_controller.get("/list", response_model=list[TransactionOutputData])
async def get_transactions(
    year: int = Query(..., ge=TRANSACTION_MINIMAL_YEAR),
    month: int = Query(..., ge=TRANSACTION_MINIMAL_MONTH, le=TRANSACTION_MAXIMAL_MONTH),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)

    return transaction_service.get_list(
        Transaction.account.has(user=current_user),
        func.DATE_PART("YEAR", Transaction.due_date) == year,
        func.DATE_PART("MONTH", Transaction.due_date) == month,
    )

@transaction_controller.get("/item", response_model=TransactionOutputData)
async def get_transaction(
    transaction_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)
    transaction: Transaction | None = transaction_service.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    return transaction

@transaction_controller.post("/create", response_model=TransactionOutputData, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    if not any(transaction_data.account_id == account.id for account in current_user.accounts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have an account with given `id`",
        )

    if not any(transaction_data.category_id == category.id for category in current_user.categories):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a category with given `id`",
        )

    transaction_service: TransactionService = TransactionService(session=session)

    return transaction_service.create(
        record_data=transaction_data,
    )

@transaction_controller.patch("/update", response_model=TransactionOutputData)
async def update_transaction(
    transaction_data: TransactionUpdateData,
    transaction_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)
    transaction: Transaction | None = transaction_service.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    return transaction_service.update(
        record=transaction,
        record_data=transaction_data,
    )

@transaction_controller.delete("/delete", response_model=str)
async def delete_transaction(
    transaction_id: PositiveInt = Query(..., alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)
    transaction: Transaction | None = transaction_service.get_by_id(transaction_id)

    if transaction is None:
        raise CouldNotFindRecord(transaction_id, Transaction)

    if transaction.account.user != current_user:
        raise CouldNotAccessRecord(transaction_id, Transaction)

    transaction_service.delete(transaction)

    return "Transaction was deleted"
