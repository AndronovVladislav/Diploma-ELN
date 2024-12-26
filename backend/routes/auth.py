import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.schemas.users import UserLogin, UserResponse, UserSignup
from backend.services.auth import create_user, get_user, hash_password

router = APIRouter(prefix='/users')

security = HTTPBasic()

unauthorized = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail='Пользователь с таким email или паролем не найден!',
    headers={"WWW-Authenticate": "Basic"},
)


async def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    user = await get_user(credentials.email)  # how to provide email?
    if user is None:
        raise unauthorized

    if not secrets.compare_digest(
        hash_password(credentials.password).encode("utf-8"),
        user.hashed_password.encode("utf-8"),
    ):
        raise unauthorized

    return credentials.email


@router.post("/login")
async def login(credentials: UserLogin) -> ...:
    ...


@router.post("/signup")
async def signup(form: UserSignup) -> UserResponse:
    user = await get_user(form.email)
    if not user:
        await create_user(form)
        return UserResponse.model_validate(user, from_attributes=True)
    return HTTPException(status.HTTP_409_CONFLICT, 'Пользователь с указанным email уже существует!')
