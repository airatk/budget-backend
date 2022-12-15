from calendar import monthrange
from datetime import date, datetime

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response


def test_get_summary(test_client: TestClient):
    response: Response = test_client.get("/trend/summary")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_get_last_n_days_highlight(test_client: TestClient):
    n_days: int = 7
    response: Response = test_client.get("/trend/last-n-days?n_days={0}".format(n_days))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 7

def test_get_monthly_trend(test_client: TestClient):
    today_date: date = datetime.today().date()
    (_, current_month_days_number) = monthrange(year=today_date.year, month=today_date.month)

    response: Response = test_client.get("/trend/current-month")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == current_month_days_number
