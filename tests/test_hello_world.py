from fastapi import status
from fastapi.testclient import TestClient

from fastzero.app import app

client = TestClient(app)
HELLO_WORLD_URL = "/hello"


def test_get_hello_is_sucess():
    response = client.get(HELLO_WORLD_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"hello": "world"}
