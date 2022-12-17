from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import CurrencyType


def test_get_balances(test_client: TestClient):
    response: Response = test_client.get("/account/balances")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()

def test_get_accounts(test_client: TestClient):
    response: Response = test_client.get("/account/list")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()

@mark.parametrize("test_account_data", (
    param(
        {
            "name": "Test Account Name",
            "currency": CurrencyType.RUB.value,
            "openning_balance": 260000,
        },
        id="correct_data",
    ),
    param(
        {
            "name": "Test Account Name",
            "currency": "non-existing currency type",
            "openning_balance": 260000,
        },
        marks=mark.xfail,
        id="incorrect_data",
    ),
    param(
        {},
        marks=mark.xfail,
        id="missing_fields",
    ),
))
def test_create_account(test_client: TestClient, test_account_data: dict[str, Any]):
    response: Response = test_client.post(
        url="/account/create",
        json=test_account_data,
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert isinstance(response.json(), dict)

    intersected_account_data: dict[str, Any] = {
        test_field: test_datum
        for (test_field, test_datum) in test_account_data.items()
        if response.json().get(test_field) == test_datum
    }

    assert isinstance(response.json().get("id"), int)
    assert intersected_account_data == test_account_data

@mark.parametrize("test_account_data", (
    param(
        {
            "id": 1,
            "name": "Test Account Name",
            "currency": CurrencyType.RUB.value,
            "openning_balance": 260000,
        },
        id="correct_data",
    ),
    param(
        {
            "id": 1,
            "currency": "non-existing currency type",
        },
        marks=mark.xfail,
        id="incorrect_data",
    ),
    param(
        {},
        marks=mark.xfail,
        id="missing_id",
    ),
))
def test_update_account(test_client: TestClient, test_account_data: dict[str, Any]):
    response: Response = test_client.patch(
        url="/account/update",
        json=test_account_data,
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), dict)

    intersected_account_data: dict[str, Any] = {
        test_field: test_datum
        for (test_field, test_datum) in test_account_data.items()
        if response.json().get(test_field) == test_datum
    }

    assert intersected_account_data == test_account_data

@mark.parametrize("account_id", (
    param(1),
    param(0, marks=mark.xfail),
    param("string", marks=mark.xfail),
    param(None, marks=mark.xfail),
))
def test_delete_account(test_client: TestClient, account_id: Any):
    response: Response = test_client.delete(
        url="/account/delete",
        params={
            "id": account_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == "Account was deleted"
