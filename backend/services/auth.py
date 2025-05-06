from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User
from backend.models.user import Profile
from backend.models.utils import connection
from backend.routes.auth.utils import (
    get_user_by_username,
    hash_password,
    validate_password,
    create_access_token,
    create_refresh_token,
)
from backend.schemas.auth import UserSignup, UserLogin


@connection
async def signup(user_data: UserSignup, session: AsyncSession) -> User:
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким username уже существует',
        )

    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
    )
    session.add(new_user)
    await session.flush()

    user_profile = Profile(user_id=new_user.id)
    session.add(user_profile)
    return new_user


async def login(credentials: UserLogin) -> tuple[str, str]:
    user = await get_user_by_username(credentials.username)
    if not (user and validate_password(credentials.password, user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные username или пароль')

    access = create_access_token(subject=user.username)
    refresh = create_refresh_token(subject=user.username)
    return access, refresh


async def refresh_token(refresh_payload: dict) -> tuple[str, str]:
    username = refresh_payload.get('sub')
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный payload токена')

    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    new_access_token = create_access_token(subject=user.username)
    new_refresh_token = create_refresh_token(subject=user.username)
    return new_access_token, new_refresh_token
