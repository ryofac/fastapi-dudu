from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from fastzero.settings import Settings

engine: Engine = create_engine(Settings().DATABASE_URL)


# Injeção de dependências: isso vai atuar como dependência nas rotas do app
def get_session():
    with Session(engine) as session:
        yield session
