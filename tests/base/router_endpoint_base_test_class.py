from typing import Any

from httpx import AsyncClient, Response
from httpx._client import USE_CLIENT_DEFAULT  # noqa: WPS436


class RouterEndpointBaseTestClass:
    http_method: str
    endpoint: str

    def __init_subclass__(
        cls,
        http_method: str,
        endpoint: str,
    ) -> None:
        super().__init_subclass__()

        cls.http_method = http_method
        cls.endpoint = endpoint

    async def request(
        self,
        test_client: AsyncClient,
        test_credentials: tuple[str, str] | None = None,
        test_data: dict[str, Any] | None = None,
        **query_parameters: Any,
    ) -> Response:
        query_parameters = {
            key: test_value
            for key, test_value in query_parameters.items()
            if test_value is not None
        }

        return await test_client.request(
            method=self.http_method,
            url=self.endpoint,
            json=test_data,
            params=query_parameters or None,
            auth=test_credentials or USE_CLIENT_DEFAULT,
        )
