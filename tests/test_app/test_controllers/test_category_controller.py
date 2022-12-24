from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import CategoryType
from tests.test_app.test_controllers.utilities.base_test_class import (
    BaseTestClass,
)


def test_get_categories(test_client: TestClient):
    response: Response = test_client.get("/category/list")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()


class TestGetCategory(BaseTestClass, http_method="GET", api_endpoint="/category/item"):
    @mark.parametrize("test_id, expected_data", (
        param(
            1,
            {
                "id": 1,
                "base_category_id": None,
                "name": "Category 1",
                "type": CategoryType.INCOME.value,
            },
            id="category_1",
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
        -1,
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


class TestCreateCategory(BaseTestClass, http_method="POST", api_endpoint="/category/create"):
    @mark.parametrize("test_data, expected_data", (
        param(
            {
                "base_category_id": None,
                "name": "Category 1",
                "type": CategoryType.INCOME.value,
            },
            {
                "id": 7,
                "base_category_id": None,
                "name": "Category 1",
                "type": CategoryType.INCOME.value,
            },
            id="category_7",
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
                "base_category_id": None,
                "name": "",
                "type": CategoryType.INCOME.value,
            },
            id="wrong_name",
        ),
        param(
            {
                "base_category_id": None,
                "name": "Category 1",
                "type": "non_existing_type",
            },
            id="wrong_type",
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


class TestUpdateAccount(BaseTestClass, http_method="PATCH", api_endpoint="/category/update"):
    @mark.parametrize("test_id, test_data, expected_data", (
        param(
            1,
            {
                "base_category_id": None,
                "name": "Category",
                "type": CategoryType.INCOME.value,
            },
            {
                "id": 1,
                "base_category_id": None,
                "name": "Category",
                "type": CategoryType.INCOME.value,
            },
            id="category_1",
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
                "name": "",
            },
            id="wrong_name",
        ),
        param(
            1,
            {
                "type": "non_existing_type",
            },
            id="wrong_type",
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
            id=test_id,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    @mark.parametrize("test_id", (
        0,
        -1,
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


class TestDeleteCategory(BaseTestClass, http_method="DELETE", api_endpoint="/category/delete"):
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
        assert response.json() == "Budget was deleted"

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
        -1,
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
