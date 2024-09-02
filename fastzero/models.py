from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


# O nome disso é REGISTRO ESCALAR:
# -> Os atributos tem que ser mapeados Mapped[tipo-python]
# Vem da álgebra escalar, transforma isso em um "objeto escalar",
# que se relaciona com as linhas DENTRO DO BANCO DE DADOS
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    # init = False => Das próximas vezes o preenchimento
    # não será passado no __init__ do dado. Isso será gerenciado
    # pelo sqlalchemy, usado para valores gerados!
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)

    # server => quem decide é o servidor, o banco de dados
    # func => funções utilitárias sql
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
