from typing import Any

from fastapi import status
from httpx import AsyncClient, Response
from pytest import mark, param

from core.databases.models.utilities.types import TransactionType
from tests.base.router_endpoint_base_test_class import (
    RouterEndpointBaseTestClass,
)


@mark.anyio
async def test_get_periods(test_client: AsyncClient) -> None:
    response: Response = await test_client.get('/transaction/periods')

    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert response.json()


class TestGetTransactions(RouterEndpointBaseTestClass, http_method='GET', endpoint='/transaction/list'):
    @mark.parametrize('test_year', (
        2022,
    ))
    @mark.parametrize('test_month', (
        12,
    ))
    @mark.anyio
    async def test_with_correct_data(
        self,
        test_client: AsyncClient,
        test_year: int,
        test_month: int,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            year=test_year,
            month=test_month,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert isinstance(response.json(), list)
        assert response.json()

    @mark.parametrize('test_year', (
        param(1999, id='lower'),
        param('string'),
        param(None),
    ))
    @mark.parametrize('test_month', (
        param(13, id='greater'),
        param(0, id='lower'),
        param('string'),
        param(None),
    ))
    @mark.anyio
    async def test_with_wrong_data(
        self,
        test_client: AsyncClient,
        test_year: Any,
        test_month: Any,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            year=test_year,
            month=test_month,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


class TestGetTransaction(RouterEndpointBaseTestClass, http_method='GET', endpoint='/transaction/item'):
    @mark.parametrize('test_id, expected_data', (
        param(
            1,
            {
                'id': 1,
                'account_id': 1,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40:00',
                'amount': 300,
                'note': 'Note',
            },
            id='transaction_1',
        ),
    ))
    @mark.anyio
    async def test_with_correct_id(
        self,
        test_client: AsyncClient,
        test_id: int,
        expected_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
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


class TestCreateTransaction(RouterEndpointBaseTestClass, http_method='POST', endpoint='/transaction/create'):
    @mark.parametrize('test_data, expected_data', (
        param(
            {
                'account_id': 1,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40:00',
                'amount': 100,
                'note': 'Note',
            },
            {
                'id': 5,
                'account_id': 1,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40:00',
                'amount': 100,
                'note': 'Note',
            },
            id='transaction_4',
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
                'account_id': 0,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_account_id',
        ),
        param(
            {
                'account_id': 1,
                'category_id': 0,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_category_id',
        ),
        param(
            {
                'account_id': 1,
                'category_id': 1,
                'type': 'non_existing_type',
                'due_date': '2022-12-12',
                'due_time': '10:40',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_type',
        ),
        param(
            {
                'account_id': 0,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '',
                'due_time': '10:40',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_due_date',
        ),
        param(
            {
                'account_id': 0,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_due_time',
        ),
        param(
            {
                'account_id': 0,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40',
                'amount': 0,
                'note': 'Note',
            },
            id='wrong_amount',
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

    @mark.parametrize('test_data', (
        param(
            {
                'account_id': 4,
                'category_id': 1,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40:00',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_account_id',
        ),
        param(
            {
                'account_id': 1,
                'category_id': 5,
                'type': TransactionType.INCOME.value,
                'due_date': '2022-12-12',
                'due_time': '10:40:00',
                'amount': 100,
                'note': 'Note',
            },
            id='wrong_category_id',
        ),
    ))
    @mark.anyio
    async def test_with_wrong_ids(
        self,
        test_client: AsyncClient,
        test_data: dict[str, Any],
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            test_data=test_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


class TestUpdateTransaction(RouterEndpointBaseTestClass, http_method='PATCH', endpoint='/transaction/update'):
    @mark.parametrize('test_id, test_data, expected_data', (
        param(
            1,
            {
                'account_id': 2,
                'category_id': 2,
                'type': TransactionType.OUTCOME.value,
                'due_date': '2022-12-24',
                'due_time': '12:40:00',
                'amount': 200,
                'note': 'New Note',
            },
            {
                'id': 1,
                'account_id': 2,
                'category_id': 2,
                'type': TransactionType.OUTCOME.value,
                'due_date': '2022-12-24',
                'due_time': '12:40:00',
                'amount': 200,
                'note': 'New Note',
            },
            id='transaction_1',
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
        assert response.json() == expected_data

    @mark.parametrize('test_id, test_data', (
        param(
            1,
            {
                'account_id': 0,
            },
            id='wrong_account_id',
        ),
        param(
            1,
            {
                'category_id': 0,
            },
            id='wrong_category_id',
        ),
        param(
            1,
            {
                'type': 'non_existing_type',
            },
            id='wrong_type',
        ),
        param(
            1,
            {
                'due_date': '',
            },
            id='wrong_due_date',
        ),
        param(
            1,
            {
                'due_time': '',
            },
            id='wrong_due_time',
        ),
        param(
            1,
            {
                'amount': 0,
            },
            id='wrong_amount',
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


class TestDeleteTransaction(RouterEndpointBaseTestClass, http_method='DELETE', endpoint='/transaction/delete'):
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
