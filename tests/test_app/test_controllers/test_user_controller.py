from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param


def test_get_current_user(test_client: TestClient):
    response: Response = test_client.get("/user/current")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {
        "id": 1,
        "family_id": 1,
        "username": "test-user",
    }


class TestGetRelative:
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
        response: Response = self._make_request(
            test_client=test_client,
            test_id=test_data["id"],
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            "id": test_data["id"],
            "family_id": 1,
            "username": test_data["username"],
        }

    def test_with_self_id(self, test_client: TestClient):
        response: Response = self._make_request(
            test_client=test_client,
            test_id=1,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
        assert response.json() == "Provided `id` belongs to the user himself"

    @mark.parametrize("test_id", (
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
    def test_failure_get_relative(self, test_client: TestClient, test_id: Any):
        response: Response = self._make_request(
            test_client=test_client,
            test_id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def _make_request(
        self,
        test_client: TestClient,
        test_id: Any,
    ) -> Response:
        return test_client.get(
            url="/user/relative",
            params={
                "id": test_id,
            },
        )
