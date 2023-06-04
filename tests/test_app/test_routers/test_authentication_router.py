from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from tests.base.router_endpoint_base_test_class import (
    RouterEndpointBaseTestClass,
)


class TestSignUp(RouterEndpointBaseTestClass, http_method='POST', endpoint='/sign-up'):
    @mark.parametrize('test_data', (
        param(
            {
                'username': 'test-user-4',
                'password': 'test-password',
            },
            id='user_4',
        ),
        param(
            {
                'username': 'test-user-5',
                'password': 'test-password',
                'family_id': 1,
            },
            id='user_5',
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json().get('user').get('username') == test_data['username']

    @mark.parametrize('test_data, expected_status_code', (
        param(
            {
                'username': '',
                'password': 'test-password',
                'family_id': 1,
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_username',
        ),
        param(
            {
                'username': 'test-user-5',
                'password': 'short',
                'family_id': 1,
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='too_short_password',
        ),
        param(
            {
                'username': 'test-user-5',
                'password': 'shortpass',
                'family_id': -1,
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_family_id',
        ),
        param(
            {
                'username': 'test-user',
                'password': 'test-password',
            },
            status.HTTP_400_BAD_REQUEST,
            id='existing_user',
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
        expected_status_code: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == expected_status_code, response.text


class TestSignIn(RouterEndpointBaseTestClass, http_method='GET', endpoint='/sign-in'):
    @mark.parametrize('test_credentials', (
        param(
            ('test-user', 'test-password'),
            id='user_1',
        ),
        param(
            ('family-member', 'test-password'),
            id='user_2',
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_credentials: tuple[str, str],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_credentials=test_credentials,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json().get('user').get('username') == test_credentials[0]

    @mark.parametrize('test_credentials, expected_status_code', (
        param(
            ('non-existing-user', 'password'),
            status.HTTP_404_NOT_FOUND,
            id='non_existing_user',
        ),
        param(
            ('test-user', 'wrong-password'),
            status.HTTP_403_FORBIDDEN,
            id='wrong_password',
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_credentials: tuple[str, str],
        expected_status_code: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_credentials=test_credentials,
        )

        assert response.status_code == expected_status_code, response.text
