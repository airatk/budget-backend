from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response


def test_get_accounts(test_client: TestClient):
    response: Response = test_client.get("/account/list")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()
