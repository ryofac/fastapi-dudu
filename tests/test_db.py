from sqlalchemy import select

from fastzero.models import User


def test_create_user(session):
    payload = {
        "username": "ryofac",
        "password": "123321",
        "email": "ryofac@gmail.com",
    }

    # Respeita o conceito de atomicidade
    # As mudanças no banco de dados vão ser feitas somente nesse contexto
    user_created = User(**payload)
    session.add(user_created)
    session.commit()
    session.refresh(user_created)

    # Busca com sql builder:
    # scalar -> pega um registro do banco de dados no formato
    # do objetos python
    user_found = session.scalar(
        select(User).where(User.username == "ryofac"),
    )

    for attr, value in payload.items():
        assert getattr(user_found, attr) == value
