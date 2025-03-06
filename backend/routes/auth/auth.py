from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.models.user import User
from backend.routes.auth.validation import get_current_refresh_payload, get_current_auth_user
from backend.schemas.auth import UserSignup, UserLogin, TokenResponse
from backend.services.auth import (
    signup as signup_service,
    login as login_service,
    refresh_token as refresh_token_service
)

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/signup')
async def signup(user_data: UserSignup):
    """
    Регистрация нового пользователя.
    """
    new_user = await signup_service(user_data)
    return {'message': f'Новый пользователь {new_user.username} зарегистрирован!'}


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """
    Вход в систему. Возвращает access и refresh токены.
    """
    access, refresh = await login_service(UserLogin(username=form_data.username, password=form_data.password))
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post('/refresh')
async def refresh_token(refresh_payload: dict = Depends(get_current_refresh_payload)) -> TokenResponse:
    """
    Эндпоинт для получения нового access/refresh токена по действующему refresh токену.
    """
    access, refresh = await refresh_token_service(refresh_payload)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.get('/me')
async def get_profile(current_user: User = Depends(get_current_auth_user)):
    """
    Пример защищённого эндпоинта, где требуется access-токен.
    """
    return {
        'username': current_user.username,
    }
