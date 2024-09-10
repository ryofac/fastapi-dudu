from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    """Esquema público de usuário (LIST, RETRIEVE)"""

    id: int
    username: str
    full_name: str | None
    email: EmailStr


class UserSchema(BaseModel):
    """Esquema base de alteração de um usuário (CREATE, UPDATE)"""

    username: str
    full_name: str | None
    email: EmailStr
    password: str


class UserList(BaseModel):
    """Esquema que representa a listagem de vários usuários"""

    users: list[UserPublic]
