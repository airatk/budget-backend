from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import Any


def get_current_month_boundaries() -> tuple[date, date]:
    today_date: date = datetime.today().date()
    current_month_days_number: int = monthrange(year=today_date.year, month=today_date.month)[1]

    current_month_first_date: date = date(year=today_date.year, month=today_date.month, day=1)
    current_month_last_date: date = date(year=today_date.year, month=today_date.month, day=current_month_days_number)

    return (current_month_first_date, current_month_last_date)

def fill_missing_dates_with_default_value(
    date_related_list: list[tuple[Any, ...]],
    default_value: Any,
    first_date: date,
    last_date: date,
) -> list[tuple[Any, ...]]:
    given_list_data: dict[date, Any] = {
        date_value: remaining_values
        for (date_value, *remaining_values) in date_related_list
    }

    full_range_of_dates: list[date] = [
        first_date + timedelta(days=day_offset)
        for day_offset in range((last_date - first_date).days + 1)
    ]

    unpackable_default_value: tuple[Any, ...] = tuple(default_value) if isinstance(default_value, (tuple, list)) else (default_value,)

    return [
        (result_list_date, *given_list_data.get(result_list_date, unpackable_default_value))
        for result_list_date in full_range_of_dates
    ]
