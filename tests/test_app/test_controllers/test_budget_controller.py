from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import BudgetType, CurrencyType


@mark.parametrize("budget_type", (
    param("personal", id="correct_data"),
    param("non_existing_budget_type", marks=mark.xfail, id="incorrect_data"),
))
def test_get_budgets(test_client: TestClient, budget_type: Any):
    response: Response = test_client.get(
        url="/budget/list",
        params={
            "type": budget_type,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()

@mark.parametrize("budget_id", (
    param(2),
    param(0, marks=mark.xfail),
    param("string", marks=mark.xfail),
    param(None, marks=mark.xfail),
))
def test_get_budget(test_client: TestClient, budget_id: Any):
    response: Response = test_client.get(
        url="/budget/item",
        params={
            "id": budget_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), dict)
    assert response.json() == {
        "id": 1,
        "name": "Budget 1",
        "planned_outcomes": 100000,
        "categories": [
            {
                "id": 5,
                "base_category_id": None,
                "name": "Category 1",
                "type": "Income",
            },
            {
                "id": 6,
                "base_category_id": None,
                "name": "Category 2",
                "type": "Outcome",
            },
        ],
    }

@mark.parametrize("test_data", (
    param(
        {
            "name": "Test Budget",
            "planned_outcomes": 10000,
            "type": BudgetType.PERSONAL.value,
            "categories_ids": [1, 2],
        },
        id="correct_data",
    ),
    param(
        {
            "name": "Test Budget",
            "planned_outcomes": 10000,
            "type": "non_existing_budget_type",
            "categories_ids": [1, 2],
        },
        marks=mark.xfail,
        id="incorrect_data",
    ),
    param(
        {
            "name": "Test Budget",
            "planned_outcomes": 10000,
            "type": BudgetType.PERSONAL.value,
            "categories_ids": [],
        },
        marks=mark.xfail,
        id="missing_category_ids",
    ),
    param(
        {},
        marks=mark.xfail,
        id="missing_fields",
    ),
))
def test_create_budget(test_client: TestClient, test_data: dict[str, Any]):
    response: Response = test_client.post(
        url="/budget/create",
        json=test_data,
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert isinstance(response.json(), dict)
    assert isinstance(response.json().get("id"), int)

@mark.parametrize("test_data", (
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
            "currency": "non_existing_currency_type",
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
def test_update_account(test_client: TestClient, test_data: dict[str, Any]):
    response: Response = test_client.patch(
        url="/budget/update",
        json=test_data,
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), dict)

    intersected_data: dict[str, Any] = {
        test_field: test_datum
        for (test_field, test_datum) in test_data.items()
        if response.json().get(test_field) == test_datum
    }

    assert intersected_data == test_data

@mark.parametrize("account_id", (
    param(1),
    param(0, marks=mark.xfail),
    param("string", marks=mark.xfail),
    param(None, marks=mark.xfail),
))
def test_delete_account(test_client: TestClient, account_id: Any):
    response: Response = test_client.delete(
        url="/budget/delete",
        params={
            "id": account_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == "Account was deleted"
