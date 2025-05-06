from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import User
from backend.models.user import Profile
from backend.models.utils import connection
from backend.schemas.user import ProfileResponse, ExperimentShortInfo, UpdateProfileRequest


@connection
async def get_profile(user: User, session: AsyncSession) -> ProfileResponse:
    q = (
        select(User).options(
            selectinload(User.experiments),
            selectinload(User.profile),
        )
        .where(User.id == user.id)
    )

    result = (await session.execute(q)).scalar_one()

    return ProfileResponse(
        username=result.username,
        name=result.profile.name,
        surname=result.profile.surname,
        email=result.profile.email,
        position=result.profile.position,
        registered_at=result.profile.registered_at,
        last_login=result.profile.last_login,
        experiments=[ExperimentShortInfo.model_validate(experiment) for experiment in result.experiments],
    )


@connection
async def edit_profile(update: UpdateProfileRequest, user: User, session: AsyncSession) -> ProfileResponse:
    q = select(Profile).where(Profile.user_id == user.id)

    profile = (await session.execute(q)).scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    update_data = update.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(profile, k, v)

    # await session.commit()
    return await get_profile(user)