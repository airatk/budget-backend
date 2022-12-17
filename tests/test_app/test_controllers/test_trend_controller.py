from calendar import monthrange
from datetime import date, datetime
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import TransactionType


def test_get_summary(test_client: TestClient):
    response: Response = test_client.get("/trend/summary")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

@mark.parametrize("n_days", (
    param(1),
    param(0, marks=mark.xfail),
    param("string", marks=mark.xfail),
    param(None, marks=mark.xfail),
))
@mark.parametrize("transaction_type", (
    param(TransactionType.INCOME.value),
    param(TransactionType.OUTCOME.value),
    param(TransactionType.TRANSFER.value),
    param("non-existing_type", marks=mark.xfail),
))
def test_get_last_n_days_highlight(test_client: TestClient, n_days: Any, transaction_type: Any):
    response: Response = test_client.get(
        url="/trend/last-n-days",
        params={
            "n_days": n_days,
            "transaction_type": transaction_type,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == n_days

def test_get_monthly_trend(test_client: TestClient):
    today_date: date = datetime.today().date()
    (_, current_month_days_number) = monthrange(year=today_date.year, month=today_date.month)

    response: Response = test_client.get("/trend/current-month")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == current_month_days_number
