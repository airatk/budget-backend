from datetime import date, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import func

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.account import (
    AccountBalanceData,
    AccountCreationData,
    AccountOutputData,
    AccountsSummaryData,
    AccountUpdateData,
    DailyHighlightData,
    PeriodSummaryData,
    SummaryPeriodType,
    TrendPointData
)
from models import Account, Transaction, User
from models.utilities.types import TransactionType


accounts_controller: APIRouter = APIRouter(prefix="/accounts")


@accounts_controller.get("/summary", response_model=list[PeriodSummaryData])
async def get_summary(
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    today_date: date = datetime.today().date()

    current_month_conditions: tuple[bool, ...] = (
        func.DATE_PART("YEAR", Transaction.due_date) == today_date.year,
        func.DATE_PART("MONTH", Transaction.due_date) == today_date.month,
    )
    current_year_conditions: tuple[bool, ...] = (
        func.DATE_PART("YEAR", Transaction.due_date) == today_date.year,
    )
    all_time_conditions: tuple[bool, ...] = ()

    transactions_sum_query: Query = session.query(
            func.SUM(Transaction.amount)
        ).\
        filter(Transaction.account.has(user=current_user))

    summary: list[PeriodSummaryData] = []

    for (period, period_conditions) in (
        (SummaryPeriodType.CURRENT_MONTH, current_month_conditions),
        (SummaryPeriodType.CURRENT_YEAR, current_year_conditions),
        (SummaryPeriodType.ALL_TIME, all_time_conditions)
    ):
        incomes: float = transactions_sum_query.filter(
                Transaction.type == TransactionType.INCOME,
                *(period_conditions or ())
            ).\
            scalar() or 0.00

        outcomes: float = transactions_sum_query.filter(
                Transaction.type == TransactionType.OUTCOME,
                *(period_conditions or ())
            ).\
            scalar() or 0.00

        accounts_summary: AccountsSummaryData = AccountsSummaryData(
            balance=incomes - outcomes,
            incomes=incomes,
            outcomes=outcomes * (-1)
        )
        period_summary: PeriodSummaryData = PeriodSummaryData(
            period=period,
            accounts_summary=accounts_summary
        )

        summary.append(period_summary)

    return summary

@accounts_controller.get("/last-n-days", response_model=list[DailyHighlightData])
async def get_last_n_days_highlight(
    n_days: PositiveInt = 7,
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    today_date: date = datetime.today().date()
    first_date: date = today_date - timedelta(days=n_days - 1)

    transactions: list[Transaction] = session.query(
            Transaction.due_date,
            func.SUM(Transaction.amount).label("amount"),
        ).\
        filter(
            Transaction.account.has(user=current_user),
            Transaction.type == transaction_type,
            Transaction.due_date.between(first_date, today_date)
        ).\
        group_by(Transaction.due_date).\
        order_by(Transaction.due_date).\
        all()

    last_n_days_highlight: list[DailyHighlightData] = []

    for day in range(first_date.day, today_date.day + 1):
        daily_highlight: DailyHighlightData = DailyHighlightData(
            date=first_date.replace(day=day),
            amount=0.00
        )

        if len(transactions) > 0 and transactions[0].due_date == daily_highlight.date:
            daily_highlight.amount = transactions[0].amount

            del transactions[0]

        last_n_days_highlight.append(daily_highlight)

    return last_n_days_highlight

@accounts_controller.get("/monthly-trend", response_model=list[TrendPointData])
async def get_monthly_trend(
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    today_date: date = datetime.today().date()

    current_month_first_date: date = today_date.replace(day=1)
    current_month_last_date: date = current_month_first_date.replace(month=current_month_first_date.month + 1) - timedelta(days=1)

    all_transactions_by_days: Any = session.query(
            Transaction.due_date.label("date"),
            func.DATE_PART("DAY", Transaction.due_date).label("day"),
            func.SUM(Transaction.amount).label("amount")
        ).\
        filter(
            Transaction.account.has(user=current_user),
            Transaction.type == transaction_type
        ).\
        group_by(Transaction.due_date).\
        subquery()

    average_trend_points: Any = session.query(
            all_transactions_by_days.c.day,
            func.AVG(all_transactions_by_days.c.amount).label("average_amount")
        ).\
        group_by(all_transactions_by_days.c.day).\
        subquery()

    trend_points: list[Any] = session.query(
            all_transactions_by_days.c.day,
            all_transactions_by_days.c.amount.label("current_month_amount"),
            average_trend_points.c.average_amount
        ).\
        join(average_trend_points, average_trend_points.c.day == all_transactions_by_days.c.day).\
        filter(all_transactions_by_days.c.date.between(current_month_first_date, current_month_last_date)).\
        order_by(all_transactions_by_days.c.day).\
        all()

    previous_trend_point: TrendPointData = TrendPointData(
        date=current_month_first_date.replace(day=current_month_first_date.day),
        current_month_amount=0.00,
        average_amount=0.00
    )
    monthly_trend: list[TrendPointData] = []

    for day in range(current_month_first_date.day, current_month_last_date.day + 1):
        current_trend_point: TrendPointData = TrendPointData(
            date=current_month_first_date.replace(day=day),
            current_month_amount=previous_trend_point.current_month_amount,
            average_amount=previous_trend_point.average_amount
        )

        if len(trend_points) > 0 and trend_points[0].day == day:
            current_trend_point.current_month_amount += trend_points[0].current_month_amount
            current_trend_point.average_amount += trend_points[0].average_amount

            del trend_points[0]

        monthly_trend.append(current_trend_point)
        previous_trend_point = current_trend_point

    return monthly_trend

@accounts_controller.get("/balances", response_model=list[AccountBalanceData])
async def get_balances(
    current_user: User = Depends(identify_user)
):
    balances: list[AccountBalanceData] = []

    for account in current_user.accounts:
        account_incomes: float = sum(
            transaction.amount for transaction in account.transactions
            if transaction.type == TransactionType.INCOME
        )
        account_outcomes: float = sum(
            transaction.amount for transaction in account.transactions
            if transaction.type == TransactionType.OUTCOME
        )

        account_balance: AccountBalanceData = AccountBalanceData(
            account=account.name,
            balance=(account.openning_balance + account_incomes) - account_outcomes
        )

        balances.append(account_balance)

    return balances

@accounts_controller.get("/list", response_model=list[AccountOutputData])
async def get_accounts(
    current_user: User = Depends(identify_user)
):
    return current_user.accounts

@accounts_controller.post("/create", response_model=AccountOutputData)
async def create_account(
    account_data: AccountCreationData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
    account: Account = Account(
        user=current_user,
        name=account_data.name,
        currency=account_data.currency,
        openning_balance=account_data.openning_balance
    )

    session.add(account)
    session.commit()

    return account

@accounts_controller.put("/update", response_model=AccountOutputData)
async def update_account(
    account_data: AccountUpdateData,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
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

    for (field, value) in account_data.dict().items():
        setattr(account, field, value)

    session.commit()

    return account

@accounts_controller.delete("/delete", response_model=str)
async def delete_account(
    id: PositiveInt,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session)
):
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
