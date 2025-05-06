from fastapi import APIRouter, Depends

from backend.models import User
from backend.routes.auth.validation import get_current_auth_user
from backend.schemas.user import ProfileResponse, UpdateProfileRequest
from backend.services.user import edit_profile as edit_profile_service, get_profile as get_profile_service

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/profile', response_model=ProfileResponse)
async def get_profile(user: User = Depends(get_current_auth_user)):
    """
    Получение профиля пользователя.
    """
    return await get_profile_service(user)


@router.patch('/profile', response_model=ProfileResponse)
async def edit_profile(payload: UpdateProfileRequest, user: User = Depends(get_current_auth_user)):
    """
    Изменение профиля пользователя.
    """
    return await edit_profile_service(payload, user)
