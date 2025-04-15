import pytest

from backend.common.enums import Role


@pytest.fixture
def login_form() -> dict:
    return {
        'username': 'test-user',
        'password': 'test-password',
    }


@pytest.fixture
def signup_form(login_form: dict) -> dict:
    return {
        **login_form,
        'role': Role.ADMIN
    }


@pytest.mark.asyncio
async def test_auth_signup(client, signup_form: dict):
    response = await client.post('/auth/signup', json=signup_form)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_auth_login(client, signup_form: dict, login_form: dict):
    await client.post('/auth/signup', json=signup_form)

    response = await client.post('/auth/login', json=login_form)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['username'] == 'test-user'


@pytest.mark.asyncio
async def test_auth_refresh(client, signup_form: dict, login_form: dict):
    await client.post('/auth/signup', json=signup_form)
    refresh_token = (await client.post('/auth/login', json=login_form)).json()['refresh_token']

    headers = {'Authorization': f'Bearer {refresh_token}'}
    refresh_response = await client.post('/auth/refresh', headers=headers)
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['username'] == 'test-user'
