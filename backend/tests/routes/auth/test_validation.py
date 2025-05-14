import pytest
from fastapi import HTTPException

from backend.models import User
from backend.routes.auth.utils import TokenType, create_access_token
from backend.routes.auth.validation import (
    get_current_token_payload,
    validate_token_type,
    get_current_auth_user,
    get_current_refresh_payload
)


@pytest.fixture
def invalid_token() -> str:
    """Создаёт невалидный токен"""
    return 'invalid.token.payload'


@pytest.mark.asyncio
async def test_get_current_auth_user(mocker, access_token: str, user: User):
    """Тестирует получение пользователя по access-токену"""
    mocker.patch('backend.routes.auth.validation.get_user_by_username', return_value=user)

    response = await get_current_auth_user(get_current_token_payload(access_token))
    assert response.username == user.username


@pytest.mark.asyncio
async def test_get_current_auth_user_not_found(access_token: str):
    """Тестирует случай, когда пользователь не найден"""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_auth_user(get_current_token_payload(create_access_token('fake_user')))
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Пользователь не найден'


@pytest.mark.parametrize('token_type', [TokenType.ACCESS, TokenType.REFRESH])
def test_validate_token_type(token_type: TokenType):
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
async def test_get_current_token_payload(token_fixture: str, expected_type: TokenType, user: User, request):
    """Тестирует декодирование валидных токенов (и access, и refresh)"""
    token = request.getfixturevalue(token_fixture)
    payload = get_current_token_payload(token)

    assert payload['sub'] == user.username
    assert payload['token_type'] == expected_type


@pytest.mark.asyncio
async def test_get_current_token_payload_invalid(invalid_token: str):
    """Тестирует обработку невалидных токенов"""
    with pytest.raises(HTTPException) as exc_info:
        get_current_token_payload(invalid_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Невалидный JWT-токен'


@pytest.mark.asyncio
async def test_get_current_refresh_payload(refresh_token: str, user: User):
    """Тестирует валидацию refresh-токена"""
    payload = get_current_refresh_payload(refresh_token)

    assert payload['sub'] == user.username
    assert payload['token_type'] == TokenType.REFRESH


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
