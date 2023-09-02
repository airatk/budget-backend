from fastapi import status
from httpx import AsyncClient, Response
from pytest import mark, param


@mark.parametrize('test_username, expected_status_code', (
    param(
        'test-user',
        status.HTTP_200_OK,
        id='family_member',
    ),
    param(
        'not-family-member',
        status.HTTP_400_BAD_REQUEST,
        id='not_family_member',
    ),
))
@mark.anyio
async def test_get_family(
    test_client: AsyncClient,
    test_username: str,
    expected_status_code: int,
) -> None:
    response: Response = await test_client.get(
        url='/family/current',
        headers={
            'test-username': test_username,
        },
    )

    assert response.status_code == expected_status_code, response.text
