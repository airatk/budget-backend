from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from models.utilities.types import BudgetType, CategoryType
from tests.test_app.utilities.controller_method_test_class import (
    ControllerMethodTestClass,
)


class TestGetBudgets(ControllerMethodTestClass, http_method="GET", api_endpoint="/budget/list"):
    @mark.parametrize("test_type, expected_items_number", (
        param(BudgetType.PERSONAL.value, 1),
        param(BudgetType.JOINT.value, 2),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_type: Any,
        expected_items_number: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            type=test_type,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert len(response.json()) == expected_items_number

    @mark.parametrize("test_type", (
        "non_existing_type",
        None,
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_type: Any,
    ):
        response: Response = self.request(
            test_client=test_client,
            type=test_type,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestGetBudget(ControllerMethodTestClass, http_method="GET", api_endpoint="/budget/item"):
    @mark.parametrize("test_id, expected_data", (
        param(
            2,
            {
                "id": 2,
                "name": "Budget 2",
                "type": BudgetType.JOINT.value,
                "planned_outcomes": 200000,
                "categories": [
                    {
                        "id": 5,
                        "base_category_id": None,
                        "name": "Category 1",
                        "type": CategoryType.INCOME.value,
                    },
                    {
                        "id": 6,
                        "base_category_id": None,
                        "name": "Category 2",
                        "type": CategoryType.OUTCOME.value,
                    },
                ],
            },
            id="budget_2",
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


class TestCreateBudget(ControllerMethodTestClass, http_method="POST", api_endpoint="/budget/create"):
    @mark.parametrize("test_data, expected_data", (
        param(
            {
                "name": "Budget 3",
                "planned_outcomes": 200000,
                "type": BudgetType.PERSONAL.value,
                "category_ids": [1],
            },
            {
                "id": 3,
                "name": "Budget 3",
                "type": BudgetType.PERSONAL.value,
                "planned_outcomes": 200000,
                "categories": [
                    {
                        "id": 1,
                        "base_category_id": None,
                        "name": "Category 1",
                        "type": CategoryType.INCOME.value,
                    },
                ],
            },
            id="budget_3",
        ),
        param(
            {
                "name": "Budget 4",
                "planned_outcomes": 200000,
                "type": BudgetType.JOINT.value,
                "category_ids": [1],
            },
            {
                "id": 4,
                "name": "Budget 4",
                "type": BudgetType.JOINT.value,
                "planned_outcomes": 200000,
                "categories": [
                    {
                        "id": 1,
                        "base_category_id": None,
                        "name": "Category 1",
                        "type": CategoryType.INCOME.value,
                    },
                ],
            },
            id="budget_4",
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
                "name": "",
                "planned_outcomes": 200000,
                "type": BudgetType.PERSONAL.value,
                "category_ids": [1],
            },
            id="wrong_name",
        ),
        param(
            {
                "name": "Budget 3",
                "planned_outcomes": -1,
                "type": BudgetType.PERSONAL.value,
                "category_ids": [1],
            },
            id="wrong_planned_outcomes",
        ),
        param(
            {
                "name": "Budget 3",
                "planned_outcomes": 200000,
                "type": "non_existing_type",
                "category_ids": [1],
            },
            id="wrong_type",
        ),
        param(
            {
                "name": "Budget 3",
                "planned_outcomes": 200000,
                "type": BudgetType.PERSONAL.value,
                "category_ids": [],
            },
            id="missing_category_ids",
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


class TestUpdateBudget(ControllerMethodTestClass, http_method="PATCH", api_endpoint="/budget/update"):
    @mark.parametrize("test_id, test_data, expected_data", (
        param(
            1,
            {
                "name": "Budget the First",
                "planned_outcomes": 100000,
                "type": BudgetType.PERSONAL.value,
                "category_ids": [1],
            },
            {
                "id": 1,
                "name": "Budget the First",
                "type": BudgetType.PERSONAL.value,
                "planned_outcomes": 100000,
                "categories": [
                    {
                        "id": 1,
                        "base_category_id": None,
                        "name": "Category 1",
                        "type": CategoryType.INCOME.value,
                    },
                ],
            },
            id="budget_1",
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
                "planned_outcomes": -1,
            },
            id="wrong_planned_outcomes",
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
                "category_ids": [],
            },
            id="missing_category_ids",
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


class TestDeleteBudget(ControllerMethodTestClass, http_method="DELETE", api_endpoint="/budget/delete"):
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

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

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
