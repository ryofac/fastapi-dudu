from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    """Esquema público de usuário (LIST, RETRIEVE)"""

    id: int
    username: str
    full_name: str | None
    email: EmailStr
    # Tentando serializar a partir dos nomes dos
    # atributos
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Esquema base de atualização de usuário (UPDATE)"""

    full_name: str | None
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    """Esquema base de criação de um usuário (CREATE)"""

    username: str
    full_name: str | None
    email: EmailStr
    password: str


class UserList(BaseModel):
    """Esquema que representa a listagem de vários usuários"""

    users: list[UserPublic]
    model_config = ConfigDict(from_attributes=True)
