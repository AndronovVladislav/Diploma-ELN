import pytest
from fastapi import HTTPException, status
from jwt import DecodeError

from backend.common.enums import Role
from backend.routes.auth.utils import decode_jwt
from backend.schemas.auth import UserSignup, UserLogin
from backend.services.auth import signup, login


@pytest.mark.asyncio
async def test_signup():
    """
    Должен успешно зарегистрировать нового пользователя.
    """
    user_data = UserSignup(username='testuser', role=Role.RESEARCHER, password='password123')
    user = await signup(user_data)

    assert user.username == 'testuser'
    assert user.role == Role.RESEARCHER
    assert user.hashed_password != 'password123'


@pytest.mark.asyncio
async def test_signup_duplicate_email():
    """
    Должен возвращать ошибку 400, если пользователь с таким email уже существует.
    """
    user_data = UserSignup(username='testuser', role=Role.RESEARCHER, password='password123')
    await signup(user_data)

    with pytest.raises(HTTPException) as exc_info:
        await signup(user_data)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert 'Пользователь с таким username уже существует' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_login():
    """
    Должен успешно залогинить пользователя и вернуть токен.
    """
    user_data = UserSignup(username='testuser', role=Role.RESEARCHER, password='password123')
    await signup(user_data)

    login_data = UserLogin(username='testuser', password='password123')
    access_token, refresh_token = await login(login_data)

    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """
    Должен возвращать ошибку 401, если введены неверные учетные данные.
    """
    user_data = UserSignup(username='testuser', role=Role.RESEARCHER, password='password123')
    await signup(user_data)

    login_data = UserLogin(username='testuser', password='wrongpassword')

    with pytest.raises(HTTPException) as exc_info:
        await login(login_data)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Неверные username или пароль' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_validate_token_valid():
    """
    Должен успешно валидировать корректный токен.
    """
    user_data = UserSignup(username='testuser', role=Role.RESEARCHER, password='password123')
    await signup(user_data)

    login_data = UserLogin(username='testuser', password='password123')
    access_token, _ = await login(login_data)

    payload = decode_jwt(access_token)
    assert payload['sub'] == 'testuser'
