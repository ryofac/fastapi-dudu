import pytest
from fastapi import status

from fastzero.schemas import UserList

CREATE_LIST_USER_URL = "/users"

PING_URL = "/ping"


@pytest.fixture
def create_user_payload() -> dict[str, str]:
    return {
        "full_name": "Ryan Faustino",
        "username": "ryofac",
        "password": "123321",
        "email": "ryofac@gmail.com",
    }


def test_ping_pong(client):
    response = client.get(PING_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"response": "pong"}


def test_list_users_is_sucessful(client, db_user):
    response = client.get(url=CREATE_LIST_USER_URL)
    user_list_schema = UserList.model_validate({
        "users": [db_user]
    }).model_dump()
    assert response.json() == user_list_schema


def test_create_user_is_sucessful(client, create_user_payload):
    response = client.post(
        url=CREATE_LIST_USER_URL,
        json=create_user_payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    create_user_payload.pop("password")
