from enum import StrEnum

from fastapi import HTTPException, status
from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import User
from backend.models.utils import connection


class ExperimentKind(StrEnum):
    LABORATORY = 'Лабораторный'
    COMPUTATIONAL = 'Вычислительный'


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


@connection
async def get_user_experiments(username: str, session: AsyncSession) -> ...:
    q = (
        select(User)
        .options(selectinload(User.lab_experiments), selectinload(User.computational_experiments))
        .filter_by(username=username))
    user = (await session.execute(q)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь с таким id не найден')

    result = []

    for exp in user.experiments:
        exp_dict = to_dict(exp)
        exp_dict['kind'] = ExperimentKind.LABORATORY if exp in user.lab_experiments else ExperimentKind.COMPUTATIONAL
        result.append(exp_dict)

    return result
