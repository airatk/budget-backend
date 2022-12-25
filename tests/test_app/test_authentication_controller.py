from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from core.security import create_token
from tests.test_app.utilities.controller_method_test_class import (
    ControllerMethodTestClass,
)


class TestSignIn(ControllerMethodTestClass, http_method="GET", api_endpoint="/sign-in"):
    @mark.parametrize("test_credentials, expected_token", (
        param(
            ("test-user", "test-password"),
            create_token(user_id=1),
            id="user_1",
        ),
        param(
            ("family-member", "test-password"),
            create_token(user_id=2),
            id="user_2",
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_credentials: tuple[str, str],
        expected_token: str,
    ):
        response: Response = self.request(
            test_client=test_client,
            test_credentials=test_credentials,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            "access_token": expected_token,
        }

    @mark.parametrize("test_credentials", (
        param(
            ("non-existing-user", "password"),
            id="non_existing_user",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_credentials: tuple[str, str],
    ):
        response: Response = self.request(
            test_client=test_client,
            test_credentials=test_credentials,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text
        assert response.json() == {
            "detail": {
                "message": "Provided creditials are wrong",
            },
        }
