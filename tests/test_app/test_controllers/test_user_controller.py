from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from tests.test_app.test_controllers.utilities.base_test_class import (
    BaseTestClass,
)


def test_get_current_user(test_client: TestClient):
    response: Response = test_client.get("/user/current")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {
        "id": 1,
        "family_id": 1,
        "username": "test-user",
    }


class TestGetRelative(BaseTestClass, http_method="GET", api_endpoint="/user/relative"):
    @mark.parametrize("test_data", (
        param(
            {
                "id": 2,
                "username": "family-member",
            },
            id="correct_id",
        ),
    ))
    def test_with_correct_id(self, test_client: TestClient, test_data: Any):
        response: Response = self.request(
            test_client=test_client,
            id=test_data["id"],
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            "id": test_data["id"],
            "family_id": 1,
            "username": test_data["username"],
        }

    def test_with_self_id(self, test_client: TestClient):
        response: Response = self.request(
            test_client=test_client,
            id=1,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
        assert response.json() == "Provided `id` belongs to the user himself"

    @mark.parametrize("test_id", (
        0,
        -1,
        "string",
        None,
    ))
    def test_with_wrong_id(self, test_client: TestClient, test_id: Any):
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
