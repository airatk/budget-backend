from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import CurrencyType


class TestGetMethods:
    def test_get_balances(self, test_client: TestClient):
        response: Response = test_client.get("/account/balances")

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert response.json()

    def test_get_accounts(self, test_client: TestClient):
        response: Response = test_client.get("/account/list")

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert response.json()


class TestCreateAccount:
    @mark.parametrize("test_data, expected_data", (
        param(
            {
                "name": "Test Account Name",
                "currency": CurrencyType.RUB.value,
                "openning_balance": 260000,
            },
            {
                "id": 5,
                "name": "Test Account Name",
                "currency": CurrencyType.RUB.value,
                "openning_balance": 260000,
            },
            id="account_5",
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() == expected_data

    @mark.parametrize("test_data", (
        param(
            {
                "name": "",
                "currency": CurrencyType.RUB.value,
                "openning_balance": 260000,
            },
            id="wrong_name",
        ),
        param(
            {
                "name": "Test Account Name",
                "currency": "non_existing_currency",
                "openning_balance": 260000,
            },
            id="wrong_currency",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    def _make_request(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
    ) -> Response:
        return test_client.post(
            url="/account/create",
            json=test_data,
        )


class TestUpdateAccount:
    @mark.parametrize("test_account_id, test_data, expected_data", (
        param(
            1,
            {
                "name": "Test Account Name",
                "currency": CurrencyType.RUB.value,
                "openning_balance": 260000,
            },
            {
                "id": 1,
                "name": "Test Account Name",
                "currency": CurrencyType.RUB.value,
                "openning_balance": 260000,
            },
            id="correct_data",
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_account_id: int,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ):
        response: Response = test_client.patch(
            url="/account/update",
            params={
                "id": test_account_id,
            },
            json=test_data,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), dict)
        assert response.json() == expected_data

    @mark.parametrize("test_account_id, test_data", (
        param(
            1,
            {
                "name": "",
            },
            id="wrong_name",
        ),
        param(
            1,
            {
                "currency": "non_existing_currency",
            },
            id="wrong_currency",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_account_id: int,
        test_data: dict[str, Any],
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    @mark.parametrize("test_account_id", (
        param(
            999999,
            id="non_existing_id",
        ),
    ))
    def test_with_non_existing_id(
        self,
        test_client: TestClient,
        test_account_id: int,
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
            test_data={},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    @mark.parametrize("test_account_id", (
        param(
            0,
            id="zero_id",
        ),
        param(
            -1,
            id="negative_id",
        ),
        param(
            "string",
            id="string_id",
        ),
        param(
            None,
            id="none_id",
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_account_id: Any,
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
            test_data={},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    def _make_request(
        self,
        test_client: TestClient,
        test_account_id: Any,
        test_data: dict[str, Any],
    ) -> Response:
        return test_client.patch(
            url="/account/update",
            params={
                "id": test_account_id,
            },
            json=test_data,
        )


class TestDeleteAccount:
    @mark.parametrize("test_account_id", (
        param(
            1,
            id="correct_id",
        ),
    ))
    def test_with_correct_id(
        self,
        test_client: TestClient,
        test_account_id: int,
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == "Account was deleted"

    @mark.parametrize("test_account_id", (
        param(
            999999,
            id="non_existing_id",
        ),
    ))
    def test_with_non_existing_id(
        self,
        test_client: TestClient,
        test_account_id: int,
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text

    @mark.parametrize("test_account_id", (
        param(
            0,
            id="zero_id",
        ),
        param(
            -1,
            id="negative_id",
        ),
        param(
            "string",
            id="string_id",
        ),
        param(
            None,
            id="none_id",
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_account_id: Any,
    ):
        response: Response = self._make_request(
            test_client=test_client,
            test_account_id=test_account_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    def _make_request(
        self,
        test_client: TestClient,
        test_account_id: Any,
    ) -> Response:
        return test_client.delete(
            url="/account/delete",
            params={
                "id": test_account_id,
            },
        )
