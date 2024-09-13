from typing import Optional  # noqa: F401

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import UserList, UserPublic, UserSchema, UserUpdate

app = FastAPI()


@app.get("/ping/", status_code=status.HTTP_200_OK)
async def hello_world():
    return {"response": "pong"}


@app.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    tags=["users"],
)
async def create_user(
    user: UserSchema, session: Session = Depends(get_session)
):
    existent_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.username)
        )
    )

    if existent_user:
        if existent_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário com esse username já existente",
            )
        elif existent_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário com esse email já existente",
            )

    db_user = User(
        full_name=user.full_name,
        username=user.username,
        password=user.password,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_model=UserList,
    tags=["users"],
)
async def list_user(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    db_users = session.scalars(select(User).offset(offset).limit(limit))
    return {"users": db_users}


@app.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
    tags=["users"],
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session),
):
    user_found = session.scalar(select(User).where(User.id == user_id))
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_found.full_name = user.full_name
    user_found.email = user.email
    user_found.password = user.password

    session.refresh(user_found)
    session.commit()
    return user_found


@app.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
    tags=["users"],
)
async def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
):
    user_found = session.scalar(select(User).where(User.id == user_id))

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user_found


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    tags=["users"],
)
async def delete_user_by_id(user_id: int, session: Session = Depends(Session)):
    user_found = session.scalar(select(User).where(User.id == user_id))
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    session.delete(user_found)
    session.commit()

    return {"message": "User deleted"}
