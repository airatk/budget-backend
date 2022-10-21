from sqlalchemy.orm import Session
from sqlalchemy import func

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.schemas.transaction import TransactionsPeriod
from app.schemas.transaction import TransactionData

from app.models import User
from app.models import Transaction


transactions_controller: APIRouter = APIRouter(prefix="/transactions")


@transactions_controller.get("/periods", response_model=list[TransactionsPeriod])
async def get_periods(current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    periods_entities: list[tuple[int, int]] = session.query(
            Transaction.account.has(user=current_user),
            func.DATE_PART("YEAR", Transaction.due_date),
            func.DATE_PART("MONTH", Transaction.due_date)
        ).\
        distinct().\
        all()
    
    return [ TransactionsPeriod(year=period_entities[0], month=period_entities[1]) for period_entities in periods_entities ]

@transactions_controller.get("/list", response_model=list[TransactionData])
async def get_transactions(year: int, month: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    transactions: list[Transaction] = session.query(Transaction).\
        filter(
            Transaction.account.has(user=current_user),
            func.DATE_PART("YEAR", Transaction.due_date) == year,
            func.DATE_PART("MONTH", Transaction.due_date) == month
        ).\
        all()
    
    return [ TransactionData.from_orm(obj=transaction) for transaction in transactions ]

@transactions_controller.get("/item", response_model=TransactionData)
async def get_transaction(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    transaction: Transaction | None = session.query(Transaction).\
        filter(
            Transaction.id == id,
            Transaction.account.has(user=current_user)
        ).\
        one_or_none()

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a transaction with given `id`"
        )

    return TransactionData.from_orm(obj=transaction)

@transactions_controller.post("/create", response_model=str)
async def create_transaction(transaction_data: TransactionData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    if not any(transaction_data.account_id == account.id for account in current_user.accounts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have an account with given `id`"
        )
    
    if not any(transaction_data.category_id == category.id for category in current_user.categories):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a category with given `id`"
        )

    transaction: Transaction = Transaction(
        account_id=transaction_data.account_id,
        category_id=transaction_data.category_id,
        type=transaction_data.type,
        due_date=transaction_data.due_date,
        due_time=transaction_data.due_time,
        amount=transaction_data.amount,
        note=transaction_data.note
    )

    session.add(transaction)
    session.commit()

    return "Transaction was created"

@transactions_controller.put("/update", response_model=str)
async def update_transaction(transaction_data: TransactionData, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    transaction: Transaction | None = session.query(Transaction).\
        filter(
            Transaction.id == transaction_data.id,
            Transaction.account(user=current_user)
        ).\
        one_or_none()

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a transaction with given `id`"
        )

    transaction.account_id = transaction_data.account_id
    transaction.category_id = transaction_data.category_id
    transaction.type = transaction_data.type
    transaction.due_date = transaction_data.due_date
    transaction.due_time = transaction_data.due_time
    transaction.amount = transaction_data.amount
    transaction.note = transaction_data.note

    session.commit()

    return "Transaction was updated"

@transactions_controller.delete("/delete", response_model=str)
async def delete_transaction(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    transaction: Transaction | None = session.query(Transaction).\
        filter(
            Transaction.id == id,
            Transaction.account(user=current_user)
        ).\
        one_or_none()

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a transaction with given `id`"
        )

    session.delete(transaction)
    session.commit()

    return "Category was deleted"
