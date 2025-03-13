from fastapi import APIRouter, Depends

from backend.routes.auth.validation import get_current_refresh_payload
from backend.schemas.auth import UserSignup, UserLogin, UserResponse
from backend.services.auth import (
    signup as signup_service,
    login as login_service,
    refresh_token as refresh_token_service
)

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/signup')
async def signup(user_data: UserSignup) -> dict:
    """
    Регистрация нового пользователя.
    """
    new_user = await signup_service(user_data)
    return {'message': f'Новый пользователь {new_user.username} зарегистрирован!'}


@router.post('/login')
async def login(user_data: UserLogin) -> UserResponse:
    """
    Вход в систему. Возвращает access и refresh токены.
    """
    access, refresh = await login_service(user_data)
    return UserResponse(username=user_data.username, access_token=access, refresh_token=refresh)


@router.post('/refresh')
async def refresh_token(refresh_payload: dict = Depends(get_current_refresh_payload)) -> UserResponse:
    """
    Эндпоинт для получения нового access/refresh токена по действующему refresh токену.
    """
    access, refresh = await refresh_token_service(refresh_payload)
    return UserResponse(username=refresh_payload.get('sub'), access_token=access, refresh_token=refresh)
