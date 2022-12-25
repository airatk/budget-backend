from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import TransactionType
from tests.test_app.test_controllers.utilities.base_test_class import (
    ControllerMethodTestClass,
)


def test_get_periods(test_client: TestClient):
    response: Response = test_client.get("/transaction/periods")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()


class TestGetTransactions(ControllerMethodTestClass, http_method="GET", api_endpoint="/transaction/list"):
    @mark.parametrize("test_year", (
        2022,
    ))
    @mark.parametrize("test_month", (
        12,
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_year: int,
        test_month: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            year=test_year,
            month=test_month,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert response.json()

    @mark.parametrize("test_year", (
        param(1999, id="lower"),
        param("string"),
        param(None),
    ))
    @mark.parametrize("test_month", (
        param(13, id="greater"),
        param(0, id="lower"),
        param("string"),
        param(None),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_year: Any,
        test_month: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            year=test_year,
            month=test_month,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestGetTransaction(ControllerMethodTestClass, http_method="GET", api_endpoint="/transaction/item"):
    @mark.parametrize("test_id, expected_data", (
        param(
            1,
            {
                "id": 1,
                "account_id": 1,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40",
                "amount": 100,
                "note": "Note",
            },
            id="transaction_1",
        ),
    ))
    def test_with_correct_id(
        self,
        test_client: TestClient,
        test_id: int,
        expected_data: dict[str, Any],
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), dict)
        assert response.json() == expected_data

    @mark.parametrize("test_id", (
        999999,
    ))
    def test_with_non_existing_id(
        self,
        test_client: TestClient,
        test_id: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    @mark.parametrize("test_id", (
        0,
        "string",
        None,
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestCreateTransaction(ControllerMethodTestClass, http_method="POST", api_endpoint="/transaction/create"):
    @mark.parametrize("test_data, expected_data", (
        param(
            {
                "account_id": 1,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40:00",
                "amount": 100,
                "note": "Note",
            },
            {
                "id": 4,
                "account_id": 1,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40:00",
                "amount": 100,
                "note": "Note",
            },
            id="transaction_4",
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ):
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() == expected_data

    @mark.parametrize("test_data", (
        param(
            {
                "account_id": 0,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40",
                "amount": 100,
                "note": "Note",
            },
            id="wrong_account_id",
        ),
        param(
            {
                "account_id": 1,
                "category_id": 0,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40",
                "amount": 100,
                "note": "Note",
            },
            id="wrong_category_id",
        ),
        param(
            {
                "account_id": 1,
                "category_id": 1,
                "type": "non_existing_type",
                "due_date": "2022-12-12",
                "due_time": "10:40",
                "amount": 100,
                "note": "Note",
            },
            id="wrong_type",
        ),
        param(
            {
                "account_id": 0,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "",
                "due_time": "10:40",
                "amount": 100,
                "note": "Note",
            },
            id="wrong_due_date",
        ),
        param(
            {
                "account_id": 0,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "",
                "amount": 100,
                "note": "Note",
            },
            id="wrong_due_time",
        ),
        param(
            {
                "account_id": 0,
                "category_id": 1,
                "type": TransactionType.INCOME.value,
                "due_date": "2022-12-12",
                "due_time": "10:40",
                "amount": 0,
                "note": "Note",
            },
            id="wrong_amount",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
    ):
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestUpdateTransaction(ControllerMethodTestClass, http_method="PATCH", api_endpoint="/transaction/update"):
    @mark.parametrize("test_id, test_data, expected_data", (
        param(
            1,
            {
                "account_id": 2,
                "category_id": 2,
                "type": TransactionType.OUTCOME.value,
                "due_date": "2022-12-24",
                "due_time": "12:40",
                "amount": 200,
                "note": "New Note",
            },
            {
                "id": 1,
                "account_id": 2,
                "category_id": 2,
                "type": TransactionType.OUTCOME.value,
                "due_date": "2022-12-24",
                "due_time": "12:40",
                "amount": 200,
                "note": "New Note",
            },
            id="transaction_1",
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_id: int,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ):
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == expected_data

    @mark.parametrize("test_id, test_data", (
        param(
            1,
            {
                "account_id": 0,
            },
            id="wrong_account_id",
        ),
        param(
            1,
            {
                "category_id": 0,
            },
            id="wrong_category_id",
        ),
        param(
            1,
            {
                "type": "non_existing_type",
            },
            id="wrong_type",
        ),
        param(
            1,
            {
                "due_date": "",
            },
            id="wrong_due_date",
        ),
        param(
            1,
            {
                "due_time": "",
            },
            id="wrong_due_time",
        ),
        param(
            1,
            {
                "amount": 0,
            },
            id="wrong_amount",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_id: int,
        test_data: dict[str, Any],
    ):
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    @mark.parametrize("test_id", (
        999999,
    ))
    def test_with_non_existing_id(
        self,
        test_client: TestClient,
        test_id: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            test_data={},
            id=test_id,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    @mark.parametrize("test_id", (
        0,
        "string",
        None,
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestDeleteTransaction(ControllerMethodTestClass, http_method="DELETE", api_endpoint="/transaction/delete"):
    @mark.parametrize("test_id", (
        1,
    ))
    def test_with_correct_id(
        self,
        test_client: TestClient,
        test_id: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == "Transaction was deleted"

    @mark.parametrize("test_id", (
        999999,
    ))
    def test_with_non_existing_id(
        self,
        test_client: TestClient,
        test_id: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    @mark.parametrize("test_id", (
        0,
        "string",
        None,
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
