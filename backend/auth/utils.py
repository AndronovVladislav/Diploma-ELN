import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import UserSignup
from config import settings
from db.users import User
from db.utils import get_session


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def encode_jwt(payload: dict,
               private_key: str = settings.jwt.private_key_path.read_text(),
               algorithm: str = settings.jwt.algorithm,
               expire_minutes: int = settings.jwt.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None,
               ) -> str:
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)
    expire = now + (expire_timedelta if expire_timedelta else timedelta(minutes=expire_minutes))

    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(token: str | bytes,
               public_key: str = settings.jwt.public_key_path.read_text(),
               algorithm: str = settings.jwt.algorithm,
               ) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


async def get_user(email: str, session: AsyncSession = Depends(get_session)) -> User | None:
    q = select(User).filter_by(email=email)
    if user := (await session.execute(q)).scalar_one_or_none():
        return user


async def create_user(signup_form: UserSignup, session: AsyncSession = Depends(get_session)) -> User:
    data = {**signup_form.model_dump(exclude=['password']), 'hashed_password': hash_password(signup_form.password)}
    user = User(**data)
    session.add(user)
    await session.commit()
    return user
