from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from backend.routes.auth.utils import (
    decode_jwt,
    TokenType,
    TOKEN_TYPE_FIELD,
    get_user_by_username
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Декодирует любой access или refresh токены.
    """
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный JWT-токен',
        ) from e

    return payload


def validate_token_type(payload: dict, expected_type: str) -> None:
    """
    Проверяет, что в декодированном токене нужный тип (access или refresh).
    """
    current_type = payload.get(TOKEN_TYPE_FIELD)
    if current_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Ожидается {expected_type}-токен, получен: {current_type}',
        )


async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)):
    """
    Используется для эндпоинтов, требующих access-токен.
    """
    validate_token_type(payload, TokenType.ACCESS)

    username: str | None = payload.get('sub')
    if not username:
        raise HTTPException(status_code=401, detail='Токен без sub (username)')

    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден',
        )

    return user


def get_current_refresh_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Зависимость для эндпоинта обновления токена, где проверяется, что токен валиден.
    """
    try:
        print(token)
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный токен',
        )

    validate_token_type(payload, TokenType.REFRESH)
    return payload
