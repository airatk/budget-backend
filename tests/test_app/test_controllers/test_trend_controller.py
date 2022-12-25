from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import TransactionType
from tests.test_app.test_controllers.utilities.base_test_class import (
    ControllerMethodTestClass,
)


def test_get_summary(test_client: TestClient):
    response: Response = test_client.get("/trend/summary")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_get_monthly_trend(test_client: TestClient, current_month_days_number: int):
    response: Response = test_client.get("/trend/current-month")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == current_month_days_number


class TestGetLastNDaysHighlight(ControllerMethodTestClass, http_method="GET", api_endpoint="/trend/last-n-days"):
    @mark.parametrize("test_n_days", (
        param(4),
        param(None, id="default"),
        param(14),
    ))
    @mark.parametrize("test_type", (
        TransactionType.INCOME.value,
        TransactionType.OUTCOME.value,
        TransactionType.TRANSFER.value,
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_n_days: int | None,
        test_type: str,
    ):
        response: Response = self.request(
            test_client=test_client,
            n_days=test_n_days,
            transaction_type=test_type,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert len(response.json()) == test_n_days or 7

    @mark.parametrize("test_n_days", (
        param(3, id="lower"),
        param(15, id="greater"),
        param("string"),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_n_days: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            n_days=test_n_days,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
