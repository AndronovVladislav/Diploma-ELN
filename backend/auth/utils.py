import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select

from auth.models import UserSignup
from config import settings
from db import async_session_factory
from db.users import User


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


async def get_user(email: str) -> User | None:
    async with async_session_factory() as session:
        q = select(User).filter_by(email=email)
        if user := (await session.execute(q)).scalar_one_or_none():
            return user


async def create_user(signup_form: UserSignup) -> User:
    async with async_session_factory() as session:
        data = {**signup_form.model_dump(exclude=['password']), 'hashed_password': hash_password(signup_form.password)}
        user = User(**data)
        session.add(user)
        await session.commit()
        return user
