from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response


def test_get_family(test_client: TestClient):
    response: Response = test_client.get("/family/current")

    assert response.status_code == status.HTTP_200_OK, response.text
