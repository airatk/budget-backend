from calendar import monthrange
from datetime import date, datetime
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from models.utilities.types import CurrencyType


def test_get_summary(test_client: TestClient):
    response: Response = test_client.get("/account/summary")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_get_last_n_days_highlight(test_client: TestClient):
    n_days: int = 7
    response: Response = test_client.get("/account/last-n-days?n_days={0}".format(n_days))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 7

def test_get_monthly_trend(test_client: TestClient):
    today_date: date = datetime.today().date()
    (_, current_month_days_number) = monthrange(year=today_date.year, month=today_date.month)

    response: Response = test_client.get("/account/monthly-trend")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == current_month_days_number

def test_get_balances(test_client: TestClient):
    response: Response = test_client.get("/account/balances")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()

def test_get_accounts(test_client: TestClient):
    response: Response = test_client.get("/account/list")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()

def test_create_account(test_client: TestClient):
    test_account_data: dict[str, Any] = {
        "name": "Test Account Name",
        "currency": CurrencyType.RUB,
        "openning_balance": 260000
    }
    response: Response = test_client.post(
        url="/account/create",
        json=test_account_data
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data: Any = response.json()

    assert isinstance(response_data, dict)

    intersected_account_data: dict[str, Any] = {
        key: value for (key, value) in test_account_data.items() if response_data.get(key) == value
    }

    assert isinstance(response_data.get("id"), int)
    assert intersected_account_data == test_account_data

def test_update_account(test_client: TestClient):
    test_account_data: dict[str, Any] = {
        "id": 1,
        "name": "Test Account Name",
        "currency": CurrencyType.RUB,
        "openning_balance": 260000
    }
    response: Response = test_client.patch(
        url="/account/update",
        json=test_account_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

    intersected_account_data: dict[str, Any] = {
        key: value for (key, value) in test_account_data.items() if response.json().get(key) == value
    }

    assert intersected_account_data == test_account_data

def test_delete_account(test_client: TestClient):
    id: int = 1
    response: Response = test_client.delete("/account/delete?id={0}".format(id))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Account was deleted"
