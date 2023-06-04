from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark, param

from core.databases.models.utilities.types import CategoryType
from tests.base.router_endpoint_base_test_class import (
    RouterEndpointBaseTestClass,
)


def test_get_categories(test_client: TestClient) -> None:
    response: Response = test_client.get('/category/list')

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()


class TestGetCategory(RouterEndpointBaseTestClass, http_method='GET', endpoint='/category/item'):
    @mark.parametrize('test_id, expected_data', (
        param(
            1,
            {
                'id': 1,
                'base_category_id': None,
                'name': 'Category 1',
                'type': CategoryType.INCOME.value,
            },
            id='category_1',
        ),
    ))
    def test_with_correct_id(
        self,
        test_client: TestClient,
        test_id: int,
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), dict)
        assert response.json() == expected_data

    @mark.parametrize('test_id, expected_status_code', (
        param(
            999999,
            status.HTTP_404_NOT_FOUND,
            id='non_existing',
        ),
        param(
            5,
            status.HTTP_403_FORBIDDEN,
            id='forbidden_id',
        ),
        param(
            0,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            'string',
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            None,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
        expected_status_code: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == expected_status_code, response.text


class TestCreateCategory(RouterEndpointBaseTestClass, http_method='POST', endpoint='/category/create'):
    @mark.parametrize('test_data, expected_data', (
        param(
            {
                'base_category_id': None,
                'name': 'Category 1',
                'type': CategoryType.INCOME.value,
            },
            {
                'id': 7,
                'base_category_id': None,
                'name': 'Category 1',
                'type': CategoryType.INCOME.value,
            },
            id='category_7',
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() == expected_data

    @mark.parametrize('test_data', (
        param(
            {
                'base_category_id': None,
                'name': '',
                'type': CategoryType.INCOME.value,
            },
            id='wrong_name',
        ),
        param(
            {
                'base_category_id': None,
                'name': 'Category 1',
                'type': 'non_existing_type',
            },
            id='wrong_type',
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestUpdateCategory(RouterEndpointBaseTestClass, http_method='PATCH', endpoint='/category/update'):
    @mark.parametrize('test_id, test_data, expected_data', (
        param(
            1,
            {
                'base_category_id': None,
                'name': 'Category',
                'type': CategoryType.INCOME.value,
            },
            {
                'id': 1,
                'base_category_id': None,
                'name': 'Category',
                'type': CategoryType.INCOME.value,
            },
            id='category_1',
        ),
    ))
    def test_with_correct_data(
        self,
        test_client: TestClient,
        test_id: int,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == expected_data

    @mark.parametrize('test_id, test_data', (
        param(
            1,
            {
                'name': '',
            },
            id='wrong_name',
        ),
        param(
            1,
            {
                'type': 'non_existing_type',
            },
            id='wrong_type',
        ),
    ))
    def test_with_wrong_data(
        self,
        test_client: TestClient,
        test_id: int,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data=test_data,
            id=test_id,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    @mark.parametrize('test_id, expected_status_code', (
        param(
            999999,
            status.HTTP_404_NOT_FOUND,
            id='non_existing',
        ),
        param(
            5,
            status.HTTP_403_FORBIDDEN,
            id='forbidden_id',
        ),
        param(
            0,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            'string',
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            None,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
        expected_status_code: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            test_data={},
            id=test_id,
        )

        assert response.status_code == expected_status_code, response.text


class TestDeleteCategory(RouterEndpointBaseTestClass, http_method='DELETE', endpoint='/category/delete'):
    @mark.parametrize('test_id', (
        1,
    ))
    def test_with_correct_id(
        self,
        test_client: TestClient,
        test_id: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    @mark.parametrize('test_id, expected_status_code', (
        param(
            999999,
            status.HTTP_404_NOT_FOUND,
            id='non_existing',
        ),
        param(
            5,
            status.HTTP_403_FORBIDDEN,
            id='forbidden_id',
        ),
        param(
            0,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            'string',
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
        param(
            None,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='wrong_id',
        ),
    ))
    def test_with_wrong_id(
        self,
        test_client: TestClient,
        test_id: Any,
        expected_status_code: int,
    ) -> None:
        response: Response = self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == expected_status_code, response.text
