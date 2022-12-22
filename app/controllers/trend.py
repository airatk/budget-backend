from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy import Boolean
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import ColumnElement, func

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.account import (
    DailyHighlightData,
    PeriodSummaryData,
    TrendPointData,
)
from models import Transaction, User
from models.utilities.types import SummaryPeriodType, TransactionType


trend_controller: APIRouter = APIRouter(prefix="/trend", tags=["trend"])


@trend_controller.get("/summary", response_model=list[PeriodSummaryData])
async def get_summary(
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    today_date: date = datetime.today().date()

    current_month_conditions: tuple[ColumnElement[Boolean], ...] = (
        func.DATE_PART("YEAR", Transaction.due_date) == today_date.year,
        func.DATE_PART("MONTH", Transaction.due_date) == today_date.month,
    )
    current_year_conditions: tuple[ColumnElement[Boolean], ...] = (
        func.DATE_PART("YEAR", Transaction.due_date) == today_date.year,
    )
    all_time_conditions: tuple[ColumnElement[Boolean], ...] = ()

    transactions_sum_query: Query = session.query(
            func.SUM(Transaction.amount),
        ).\
        filter(Transaction.account.has(user=current_user))

    summary: list[PeriodSummaryData] = []

    for (period, period_conditions) in (
        (SummaryPeriodType.CURRENT_MONTH, current_month_conditions),
        (SummaryPeriodType.CURRENT_YEAR, current_year_conditions),
        (SummaryPeriodType.ALL_TIME, all_time_conditions),
    ):
        incomes: float = transactions_sum_query.filter(
                Transaction.type == TransactionType.INCOME,
                *period_conditions,
            ).\
            scalar() or 0.00

        outcomes: float = transactions_sum_query.filter(
                Transaction.type == TransactionType.OUTCOME,
                *period_conditions,
            ).\
            scalar() or 0

        period_summary: PeriodSummaryData = PeriodSummaryData(
            period=period,
            balance=incomes - outcomes,
            incomes=incomes,
            outcomes=outcomes * (-1),
        )

        summary.append(period_summary)

    return summary

@trend_controller.get("/last-n-days", response_model=list[DailyHighlightData])
async def get_last_n_days_highlight(
    n_days: PositiveInt = 7,
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
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
            Transaction.due_date.between(first_date, today_date),
        ).\
        group_by(Transaction.due_date).\
        order_by(Transaction.due_date).\
        all()

    last_n_days_highlight: list[DailyHighlightData] = []

    for day in range(first_date.day, today_date.day + 1):
        daily_highlight: DailyHighlightData = DailyHighlightData(
            date=first_date.replace(day=day),
            amount=0,
        )

        if transactions and transactions[0].due_date == daily_highlight.date:
            daily_highlight.amount = transactions[0].amount

            transactions.pop(0)

        last_n_days_highlight.append(daily_highlight)

    return last_n_days_highlight

@trend_controller.get("/current-month", response_model=list[TrendPointData])
async def get_current_month(
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: Session = Depends(define_postgres_session),
):
    today_date: date = datetime.today().date()
    (_, current_month_days_number) = monthrange(year=today_date.year, month=today_date.month)
    current_month_first_date: date = date(year=today_date.year, month=today_date.month, day=1)
    current_month_last_date: date = date(year=today_date.year, month=today_date.month, day=current_month_days_number)

    all_transactions_by_days: Any = session.query(
            Transaction.due_date.label("date"),
            func.DATE_PART("DAY", Transaction.due_date).label("day"),
            func.SUM(Transaction.amount).label("amount"),
        ).\
        filter(
            Transaction.account.has(user=current_user),
            Transaction.type == transaction_type,
        ).\
        group_by(Transaction.due_date).\
        subquery()

    average_trend_points: Any = session.query(
            all_transactions_by_days.c.day,
            func.AVG(all_transactions_by_days.c.amount).label("average_amount"),
        ).\
        group_by(all_transactions_by_days.c.day).\
        subquery()

    trend_points: list[Any] = session.query(
            all_transactions_by_days.c.day,
            all_transactions_by_days.c.amount.label("current_month_amount"),
            average_trend_points.c.average_amount,
        ).\
        join(average_trend_points, average_trend_points.c.day == all_transactions_by_days.c.day).\
        filter(all_transactions_by_days.c.date.between(current_month_first_date, current_month_last_date)).\
        order_by(all_transactions_by_days.c.day).\
        all()

    previous_trend_point: TrendPointData = TrendPointData(
        date=current_month_first_date,
        current_month_amount=0,
        average_amount=0,
    )
    current_month_trend: list[TrendPointData] = []

    for day in range(1, current_month_days_number + 1):
        current_trend_point: TrendPointData = TrendPointData(
            date=current_month_first_date.replace(day=day),
            current_month_amount=previous_trend_point.current_month_amount,
            average_amount=previous_trend_point.average_amount,
        )

        if trend_points and trend_points[0].day == day:
            current_trend_point.current_month_amount += trend_points[0].current_month_amount
            current_trend_point.average_amount += trend_points[0].average_amount

            trend_points.pop(0)

        current_month_trend.append(current_trend_point)
        previous_trend_point = current_trend_point

    return current_month_trend
