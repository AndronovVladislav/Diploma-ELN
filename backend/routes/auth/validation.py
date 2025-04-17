from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from backend.models import User
from backend.routes.auth.utils import (
    decode_jwt,
    TokenType,
    TOKEN_TYPE_FIELD,
    get_user_by_username
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/signin')


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Декодирует access или refresh токен.
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
    Проверяет, что в декодированном токене нужный тип.
    """
    current_type = payload.get(TOKEN_TYPE_FIELD)
    if current_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Ожидается {expected_type}-токен, получен: {current_type}',
        )


async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> User:
    """
    Используется для эндпоинтов, требующих access-токен.
    """
    validate_token_type(payload, TokenType.ACCESS)

    username: str = payload['sub']
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден',
        )

    return user


def get_current_refresh_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Зависимость для эндпоинта обновления токена. Проверяет, что токен валиден.
    """
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный токен',
        ) from e

    validate_token_type(payload, TokenType.REFRESH)
    return payload
