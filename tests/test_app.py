from fastapi import status

HELLO_WORLD_URL = "/hello"


def test_get_hello_is_sucess(client):
    response = client.get(HELLO_WORLD_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"hello": "world"}
