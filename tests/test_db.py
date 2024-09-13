from sqlalchemy import select

from fastzero.models import User

CREATE_LIST_USER_URL = "/users"


def test_create_db_user_is_sucessful(session, db_user):
    # Busca com sql builder:
    # scalar -> pega um registro do banco de dados no formato
    # do objetos python
    user_found = session.scalar(
        select(User).where(User.username == db_user.username),
    )
    assert user_found is not None
