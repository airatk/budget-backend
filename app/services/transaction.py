from datetime import date, datetime
from typing import cast

from sqlalchemy import Boolean, func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import ColumnElement, Select, Subquery

from core.calendar import (
    fill_missing_dates_with_default_value,
    get_current_month_boundaries,
)
from models import Transaction, User
from models.utilities.types import SummaryPeriodType, TransactionType

from .utilities.base import BaseService


class TransactionService(BaseService[Transaction]):
    def __init__(self, session: Session):
        super().__init__(
            model_class=Transaction,
            session=session,
        )

    def get_user_transaction_periods(self, user: User) -> list[tuple[int, int]]:
        query: Select = select(
            func.DATE_PART("YEAR", Transaction.due_date),
            func.DATE_PART("MONTH", Transaction.due_date),
        ).where(
            Transaction.account.has(user=user),
        )

        return cast(
            list[tuple[int, int]],
            self.session.execute(query).unique().all(),
        )

    def get_user_transactions_sum_for_summary_period(
        self,
        user: User,
        transactions_type: TransactionType,
        summary_period_type: SummaryPeriodType,
    ) -> float:
        period_conditions: list[ColumnElement[Boolean]] = []
        today_date: date = datetime.today().date()

        if summary_period_type in {SummaryPeriodType.CURRENT_YEAR, SummaryPeriodType.CURRENT_MONTH}:
            period_conditions.append(func.DATE_PART("YEAR", Transaction.due_date) == today_date.year)

        if summary_period_type is SummaryPeriodType.CURRENT_MONTH:
            period_conditions.append(func.DATE_PART("MONTH", Transaction.due_date) == today_date.month)

        query: Select = select(
            func.SUM(Transaction.amount),
        ).where(
            Transaction.account.has(user=user),
            Transaction.type == transactions_type,
            *period_conditions,
        )

        return self.session.scalar(query) or 0

    def get_user_transaction_sums_by_dates(
        self,
        user: User,
        transaction_type: TransactionType,
        first_date: date,
        last_date: date,
    ) -> list[tuple[date, float]]:
        query: Select = select(
            Transaction.due_date.label("date"),
            func.SUM(Transaction.amount).label("sum"),
        ).where(
            Transaction.account.has(user=user),
            Transaction.type == transaction_type,
            Transaction.due_date.between(first_date, last_date),
        ).group_by(
            Transaction.due_date,
        ).order_by(
            Transaction.due_date,
        )

        return fill_missing_dates_with_default_value(  # type: ignore [return-value]
            date_related_list=self.session.execute(query).all(),  # type: ignore [arg-type]
            default_value=0,
            first_date=first_date,
            last_date=last_date,
        )

    def get_current_month_user_transaction_statistics(
        self,
        user: User,
        transaction_type: TransactionType,
    ) -> list[tuple[date, float, float]]:
        current_month_query: Subquery = select(
            func.DATE_PART("DAY", Transaction.due_date).label("day"),
            Transaction.due_date.label("date"),
            func.SUM(Transaction.amount).label("amount"),
        ).where(
            Transaction.account.has(user=user),
            Transaction.type == transaction_type,
        ).group_by(
            Transaction.due_date,
        ).subquery()

        average_month_query: Subquery = select(
            current_month_query.c.day,
            func.AVG(current_month_query.c.amount).label("average_amount"),
        ).group_by(
            current_month_query.c.day,
        ).subquery()

        (first_date, last_date) = get_current_month_boundaries()

        transaction_statistics_query: Select = select(
            current_month_query.c.date,
            current_month_query.c.amount.label("current_amount"),
            average_month_query.c.average_amount,
        ).join(
            average_month_query,
            average_month_query.c.day == current_month_query.c.day,
        ).where(
            current_month_query.c.date.between(first_date, last_date),
        ).order_by(
            current_month_query.c.day,
        )

        return fill_missing_dates_with_default_value(  # type: ignore [return-value]
            date_related_list=self.session.execute(transaction_statistics_query).all(),  # type: ignore [arg-type]
            default_value=(0, 0),
            first_date=first_date,
            last_date=last_date,
        )
