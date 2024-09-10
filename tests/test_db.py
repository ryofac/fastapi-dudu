import pytest
from fastapi import status
from sqlalchemy import select

from fastzero.models import User

CREATE_LIST_USER_URL = "/users"


@pytest.fixture
def create_user_payload() -> dict[str, str]:
    return {
        "full_name": "Ryan Faustino",
        "username": "ryofac",
        "password": "123321",
        "email": "ryofac@gmail.com",
    }


def test_create_db_user_is_sucessful(session, create_user_payload):
    # Respeita o conceito de atomicidade
    # As mudanças no banco de dados vão ser feitas somente nesse contexto
    user_created = User(**create_user_payload)
    session.add(user_created)
    session.commit()
    session.refresh(user_created)

    # Busca com sql builder:
    # scalar -> pega um registro do banco de dados no formato
    # do objetos python
    user_found = session.scalar(
        select(User).where(User.username == "ryofac"),
    )

    for attr, value in create_user_payload.items():
        assert getattr(user_found, attr) == value


def test_create_user_is_sucessful(client, create_user_payload):
    response = client.post(
        url=CREATE_LIST_USER_URL,
        json=create_user_payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    create_user_payload.pop("password")
    assert all([
        response_parameter in response.json()
        and response.json()[response_parameter]
        == create_user_payload[response_parameter]
        for response_parameter in create_user_payload
    ])
