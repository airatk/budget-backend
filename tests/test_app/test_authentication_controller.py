from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from app.utilities.security.jwt import create_access_token
from tests.test_app.utilities.controller_method_test_class import (
    ControllerMethodTestClass,
)


class TestSignIn(ControllerMethodTestClass, http_method="GET", api_endpoint="/sign-in"):
    @mark.parametrize("test_credentials, expected_token", (
        param(
            ("test-user", "test-password"),
            create_access_token(user_id=1),
            id="user_1",
        ),
        param(
            ("family-member", "test-password"),
            create_access_token(user_id=2),
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

    @mark.parametrize("test_credentials, expected_status_code", (
        param(
            ("non-existing-user", "password"),
            status.HTTP_404_NOT_FOUND,
            id="non_existing_user",
        ),
        param(
            ("test-user", "wrong-password"),
            status.HTTP_403_FORBIDDEN,
            id="wrong_password",
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_credentials: tuple[str, str],
        expected_status_code: int,
    ):
        response: Response = self.request(
            test_client=test_client,
            test_credentials=test_credentials,
        )

        assert response.status_code == expected_status_code, response.text
