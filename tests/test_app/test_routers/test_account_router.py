from typing import Any

from fastapi import status
from httpx import AsyncClient, Response
from pytest import mark, param

from core.databases.models.utilities.types import CurrencyType
from tests.base.router_endpoint_base_test_class import (
    RouterEndpointBaseTestClass,
)


@mark.anyio
async def test_get_balances(test_client: AsyncClient) -> None:
    response: Response = await test_client.get('/account/balances')

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()

@mark.anyio
async def test_get_accounts(test_client: AsyncClient) -> None:
    response: Response = await test_client.get('/account/list')

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()


class TestCreateAccount(RouterEndpointBaseTestClass, http_method='POST', endpoint='/account/create'):
    @mark.parametrize('test_data, expected_data', (
        param(
            {
                'name': 'Test Account Name',
                'currency': CurrencyType.RUB.value,
                'opening_balance': 260000,
            },
            {
                'id': 5,
                'name': 'Test Account Name',
                'currency': CurrencyType.RUB.value,
                'opening_balance': 260000,
            },
            id='account_5',
        ),
    ))
    @mark.anyio
    async def test_with_correct_data(
        self,
        test_client: AsyncClient,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() == expected_data

    @mark.parametrize('test_data', (
        param(
            {
                'name': '',
                'currency': CurrencyType.RUB.value,
                'opening_balance': 260000,
            },
            id='wrong_name',
        ),
        param(
            {
                'name': 'Test Account Name',
                'currency': 'non_existing_type',
                'opening_balance': 260000,
            },
            id='wrong_currency',
        ),
    ))
    @mark.anyio
    async def test_with_wrong_data(
        self,
        test_client: AsyncClient,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestUpdateAccount(RouterEndpointBaseTestClass, http_method='PATCH', endpoint='/account/update'):
    @mark.parametrize('test_id, test_data, expected_data', (
        param(
            1,
            {
                'name': 'Test Account Name',
                'currency': CurrencyType.RUB.value,
                'opening_balance': 260000,
            },
            {
                'id': 1,
                'name': 'Test Account Name',
                'currency': CurrencyType.RUB.value,
                'opening_balance': 260000,
            },
            id='correct_data',
        ),
    ))
    @mark.anyio
    async def test_with_correct_data(
        self,
        test_client: AsyncClient,
        test_id: int,
        test_data: dict[str, Any],
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            test_data=test_data,
            id=test_id,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), dict)
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
                'currency': 'non_existing_type',
            },
            id='wrong_currency',
        ),
    ))
    @mark.anyio
    async def test_with_wrong_data(
        self,
        test_client: AsyncClient,
        test_id: int,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
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
            4,
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
    @mark.anyio
    async def test_with_wrong_id(
        self,
        test_client: AsyncClient,
        test_id: Any,
        expected_status_code: int,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            test_data={},
            id=test_id,
        )

        assert response.status_code == expected_status_code, response.text


class TestDeleteAccount(RouterEndpointBaseTestClass, http_method='DELETE', endpoint='/account/delete'):
    @mark.parametrize('test_id', (
        1,
    ))
    @mark.anyio
    async def test_with_correct_id(
        self,
        test_client: AsyncClient,
        test_id: int,
    ) -> None:
        response: Response = await self.request(
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
            4,
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
    @mark.anyio
    async def test_with_wrong_id(
        self,
        test_client: AsyncClient,
        test_id: Any,
        expected_status_code: int,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            id=test_id,
        )

        assert response.status_code == expected_status_code, response.text
