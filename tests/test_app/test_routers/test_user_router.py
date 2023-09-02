from typing import Any

from fastapi import status
from httpx import AsyncClient, Response
from pytest import mark, param

from tests.base.router_endpoint_base_test_class import (
    RouterEndpointBaseTestClass,
)


@mark.anyio
async def test_get_current_user(test_client: AsyncClient) -> None:
    response: Response = await test_client.get('/user/current')

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {
        'id': 1,
        'family_id': 1,
        'username': 'test-user',
    }


class TestGetRelative(RouterEndpointBaseTestClass, http_method='GET', endpoint='/user/relative'):
    @mark.parametrize('test_data', (
        param(
            {
                'id': 2,
                'username': 'family-member',
            },
            id='correct_id',
        ),
    ))
    @mark.anyio
    async def test_with_correct_id(
        self,
        test_client: AsyncClient,
        test_data: Any,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            id=test_data['id'],
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            'id': test_data['id'],
            'family_id': 1,
            'username': test_data['username'],
        }

    @mark.anyio
    async def test_with_self_id(
        self,
        test_client: AsyncClient,
    ) -> None:
        response: Response = await self.request(
            test_client=test_client,
            id=1,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
        assert response.json() == {
            'detail': {
                'message': 'Provided `id` belongs to the user himself',
            },
        }

    @mark.parametrize('test_id, expected_status_code', (
        param(
            999999,
            status.HTTP_404_NOT_FOUND,
            id='non_existing',
        ),
        param(
            3,
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
