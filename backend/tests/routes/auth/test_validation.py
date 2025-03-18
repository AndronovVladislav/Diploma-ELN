from datetime import timedelta

import pytest
from fastapi import HTTPException

from backend.models import User
from backend.routes.auth.utils import TokenType, create_jwt
from backend.routes.auth.validation import (
    get_current_token_payload,
    validate_token_type,
    get_current_auth_user,
    get_current_refresh_payload
)


@pytest.fixture
def access_token():
    """Создаёт валидный access-токен"""
    return create_jwt('test_user', TokenType.ACCESS, timedelta(minutes=1))


@pytest.fixture
def refresh_token():
    """Создаёт валидный refresh-токен"""
    return create_jwt('test_user', TokenType.REFRESH, timedelta(minutes=5))


@pytest.fixture
def invalid_token():
    """Создаёт невалидный токен"""
    return 'invalid.token.payload'


@pytest.mark.asyncio
async def test_get_current_auth_user(mocker, access_token):
    """Тестирует получение пользователя по access-токену"""
    mock_user = User(username='test_user')
    mocker.patch('backend.routes.auth.validation.get_user_by_username', return_value=mock_user)

    user = await get_current_auth_user(get_current_token_payload(access_token))
    assert user.username == 'test_user'


@pytest.mark.asyncio
async def test_get_current_auth_user_not_found(access_token):
    """Тестирует случай, когда пользователь не найден"""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_auth_user(get_current_token_payload(access_token))
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Пользователь не найден'


@pytest.mark.parametrize('token_type', [TokenType.ACCESS, TokenType.REFRESH])
def test_validate_token_type(token_type):
    """Проверяет, что функция валидирует правильный тип токена и выбрасывает ошибку для неправильного"""
    payload = {'token_type': token_type}
    validate_token_type(payload, token_type)

    with pytest.raises(HTTPException) as exc_info:
        validate_token_type(payload, TokenType.ACCESS if token_type == TokenType.REFRESH else TokenType.REFRESH)

    assert exc_info.value.status_code == 401


@pytest.mark.parametrize('token_fixture, expected_type', [
    ('access_token', TokenType.ACCESS),
    ('refresh_token', TokenType.REFRESH)
])
@pytest.mark.asyncio
async def test_get_current_token_payload(token_fixture, expected_type, request):
    """Тестирует декодирование валидных токенов (и access, и refresh)"""
    token = request.getfixturevalue(token_fixture)
    payload = get_current_token_payload(token)

    assert payload['sub'] == 'test_user'
    assert payload['token_type'] == expected_type


@pytest.mark.parametrize('token_fixture, expected_status, expected_detail', [
    ('invalid_token', 401, 'Невалидный JWT-токен'),
])
@pytest.mark.asyncio
async def test_get_current_token_payload_invalid(token_fixture, expected_status, expected_detail, request):
    """Тестирует обработку невалидных токенов"""
    token = request.getfixturevalue(token_fixture)

    with pytest.raises(HTTPException) as exc_info:
        get_current_token_payload(token)

    assert exc_info.value.status_code == expected_status
    assert exc_info.value.detail == expected_detail


@pytest.mark.parametrize('token_fixture, expected_type', [
    ('refresh_token', TokenType.REFRESH)
])
@pytest.mark.asyncio
async def test_get_current_refresh_payload(token_fixture, expected_type, request):
    """Тестирует валидацию refresh-токена"""
    token = request.getfixturevalue(token_fixture)
    payload = get_current_refresh_payload(token)

    assert payload['sub'] == 'test_user'
    assert payload['token_type'] == expected_type


@pytest.mark.parametrize('token_fixture, expected_status, expected_detail', [
    ('invalid_token', 401, 'Невалидный токен'),
])
@pytest.mark.asyncio
async def test_get_current_refresh_payload_invalid(token_fixture, expected_status, expected_detail, request):
    """Тестирует обработку невалидного refresh-токена"""
    token = request.getfixturevalue(token_fixture)

    with pytest.raises(HTTPException) as exc_info:
        get_current_refresh_payload(token)

    assert exc_info.value.status_code == expected_status
    assert exc_info.value.detail == expected_detail
