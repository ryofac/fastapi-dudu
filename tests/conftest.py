from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import User, table_registry


@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        # levando essa sessão cofigurada em memória para os testes

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session) -> Generator[TestClient, None, None]:
    # A dependência de sessão é uma função
    def get_session_override():
        return session

    # Injeta a sessão criada em memória dentro das rotas do app
    # Isso para não acessar a sessão real do banco de dados
    # Essa é uma das vantagens do modelo de injeção de dependências
    with TestClient(app) as test_client:
        app.dependency_overrides[get_session] = get_session_override
        yield test_client

    # Dependency overrides é um dicionario
    # Assegura que após cada teste isso é resetado
    app.dependency_overrides.clear()


@pytest.fixture
def db_user(session) -> User:
    db_user = User(
        username="teste",
        email="teste@email.com",
        full_name="TESTE TESTE",
        password="123321",
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
