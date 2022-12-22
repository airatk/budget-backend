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
from models import Transaction, User


transaction_controller: APIRouter = APIRouter(prefix="/transaction", tags=["transaction"])


@transaction_controller.get("/periods", response_model=list[TransactionsPeriod])
async def get_periods(
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    periods_entities: list[tuple[int, int]] = session.query(
            Transaction.account.has(user=current_user),
            func.DATE_PART("YEAR", Transaction.due_date),
            func.DATE_PART("MONTH", Transaction.due_date),
        ).\
        distinct().\
        all()

    return [TransactionsPeriod(year=period_entities[0], month=period_entities[1]) for period_entities in periods_entities]

@transaction_controller.get("/list", response_model=list[TransactionOutputData])
async def get_transactions(
    year: PositiveInt,
    month: PositiveInt,
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
    transaction_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)

    return transaction_service.get_by_id(
        transaction_id,
        Transaction.account.has(user=current_user),
    )

@transaction_controller.post("/create", response_model=TransactionOutputData)
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

@transaction_controller.put("/update", response_model=TransactionOutputData)
async def update_transaction(
    transaction_data: TransactionUpdateData,
    transaction_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)

    return transaction_service.update(
        transaction_id,
        transaction_data,
        Transaction.account(user=current_user),
    )

@transaction_controller.delete("/delete", response_model=str)
async def delete_transaction(
    transaction_id: PositiveInt = Query(alias="id"),
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    transaction_service: TransactionService = TransactionService(session=session)

    transaction_service.delete(
        transaction_id,
        Transaction.account(user=current_user),
    )

    return "Category was deleted"
