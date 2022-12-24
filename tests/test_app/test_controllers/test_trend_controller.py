from calendar import monthrange
from datetime import date, datetime
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import TransactionType
from tests.test_app.test_controllers.utilities.base_test_class import (
    BaseTestClass,
)


def test_get_summary(test_client: TestClient):
    response: Response = test_client.get("/trend/summary")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_get_monthly_trend(test_client: TestClient):
    today_date: date = datetime.today().date()
    (_, current_month_days_number) = monthrange(year=today_date.year, month=today_date.month)

    response: Response = test_client.get("/trend/current-month")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == current_month_days_number


class TestGetLastNDaysHighlight(BaseTestClass, http_method="GET", api_endpoint="/trend/last-n-days"):
    @mark.parametrize("test_n_days", (
        4,
        None,
        14,
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
        assert len(response.json()) == test_n_days

    @mark.parametrize("test_n_days", (
        param(
            3,
            id="lower",
        ),
        param(
            15,
            id="greater",
        ),
        param(
            "string",
            id="string_id",
        ),
        param(
            None,
            id="with_no_id",
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_n_days: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            n_days=test_n_days,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
