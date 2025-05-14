import datetime

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import Role
from backend.models import User, Profile
from backend.models.utils import connection
from backend.schemas.user import UpdateProfileRequest
from backend.services.user import get_profile, edit_profile


@pytest.fixture
async def profile(user: User) -> Profile:
    @connection
    async def create_profile(session: AsyncSession) -> Profile:
        profile_data = Profile(
            user_id=user.id,
            name='John',
            surname='Doe',
            email='john.doe@example.com',
            position='Developer',
            registered_at=datetime.datetime(2021, 1, 1),
            last_login=datetime.datetime(2021, 1, 1),
        )
        session.add(profile_data)
        return profile_data

    return await create_profile()


@pytest.fixture
async def nonexistent_user() -> User:
    @connection
    async def create_user(session: AsyncSession) -> User:
        user = User(username='nonexistentuser', hashed_password='xxx', role=Role.RESEARCHER)
        session.add(user)
        return user

    return await create_user()


@pytest.mark.asyncio
async def test_get_profile(user: User, profile: Profile):
    """
    Должен успешно вернуть профиль пользователя.
    """
    profile_response = await get_profile(user)

    assert profile_response.username == user.username
    assert profile_response.name == 'John'
    assert profile_response.surname == 'Doe'
    assert profile_response.email == 'john.doe@example.com'
    assert profile_response.position == 'Developer'


@pytest.mark.asyncio
async def test_edit_profile(user: User, profile: Profile):
    """
    Должен успешно обновить данные профиля пользователя.
    """
    update_data = UpdateProfileRequest(
        name='Updated Name',
        surname='Updated Surname',
        email='updated.email@example.com',
        position='Updated Position',
    )

    updated_profile = await edit_profile(update_data, user)

    assert updated_profile.name == 'Updated Name'
    assert updated_profile.surname == 'Updated Surname'
    assert updated_profile.email == 'updated.email@example.com'
    assert updated_profile.position == 'Updated Position'


@pytest.mark.asyncio
async def test_edit_profile_not_found(nonexistent_user: User):
    """
    Должен возвращать 404 ошибку, если профиль пользователя не найден при обновлении.
    """
    update_data = UpdateProfileRequest(
        name='New Name',
        surname='New Surname',
        email='new.email@example.com',
        position='New Position',
    )

    with pytest.raises(HTTPException) as exc_info:
        await edit_profile(update_data, nonexistent_user)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Пользователь с таким id не найден' in str(exc_info.value.detail)
