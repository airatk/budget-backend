from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from app.schemas.account import (
    DailyHighlightData,
    PeriodSummaryData,
    TrendPointData,
)
from core.databases.models import User
from core.databases.models.utilities.types import (
    SummaryPeriodType,
    TransactionType,
)
from core.databases.repositories import TransactionRepository


MIN_HIGHLIGHT_DAYS: int = 4
MAX_HIGHLIGHT_DAYS: int = 14


trend_router: APIRouter = APIRouter(prefix='/trend', tags=['trend'])


@trend_router.get('/summary', response_model=list[PeriodSummaryData])
async def get_summary(
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[PeriodSummaryData]:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)

    return [
        PeriodSummaryData(
            period=summary_period_type,
            incomes=await transaction_repository.get_user_transactions_sum_for_summary_period(
                user=current_user,
                transactions_type=TransactionType.INCOME,
                summary_period_type=summary_period_type,
            ),
            outcomes=await transaction_repository.get_user_transactions_sum_for_summary_period(
                user=current_user,
                transactions_type=TransactionType.OUTCOME,
                summary_period_type=summary_period_type,
            ),
        ) for summary_period_type in SummaryPeriodType
    ]

@trend_router.get('/last-n-days', response_model=list[DailyHighlightData])
async def get_last_n_days_highlight(
    n_days: int = Query(7, ge=MIN_HIGHLIGHT_DAYS, le=MAX_HIGHLIGHT_DAYS),
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[DailyHighlightData]:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)

    today_date: date = datetime.today().date()
    first_date: date = today_date - timedelta(days=n_days - 1)

    return [
        DailyHighlightData(
            date=transaction_date,
            amount=transaction_sum,
        ) for (transaction_date, transaction_sum) in await transaction_repository.get_user_transaction_sums_by_dates(
            user=current_user,
            transaction_type=transaction_type,
            first_date=first_date,
            last_date=today_date,
        )
    ]

@trend_router.get('/current-month', response_model=list[TrendPointData])
async def get_current_month(  # noqa: WPS210
    transaction_type: TransactionType = TransactionType.OUTCOME,
    current_user: User = Depends(identify_user),
    session: AsyncSession = Depends(define_postgres_session),
) -> list[TrendPointData]:
    transaction_repository: TransactionRepository = TransactionRepository(session=session)

    trend: list[TrendPointData] = []
    statistics: list[tuple[date, float, float]] = await transaction_repository.get_current_month_user_transaction_statistics(
        user=current_user,
        transaction_type=transaction_type,
    )

    previous_trend_point: TrendPointData = TrendPointData(
        date=datetime.today().date().replace(day=1),
        current_amount=0,
        average_amount=0,
    )

    for (current_date, current_amount, average_amount) in statistics:
        current_trend_point: TrendPointData = TrendPointData(
            date=current_date,
            current_amount=previous_trend_point.current_amount,
            average_amount=previous_trend_point.average_amount,
        )

        current_trend_point.current_amount += current_amount
        current_trend_point.average_amount += average_amount

        trend.append(current_trend_point)

        previous_trend_point = current_trend_point

    return trend
