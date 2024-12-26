import hashlib

from sqlalchemy import select

from backend.schemas.users import UserSignup
from models import async_session_factory
from models.users import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password).hexdigest()


async def get_user(email: str) -> User | None:
    async with async_session_factory() as session:
        q = select(User).filter_by(email=email)
        return (await session.execute(q)).one_or_none()


async def create_user(signup_form: UserSignup) -> User:
    async with async_session_factory() as session:
        data = {**signup_form, 'hashed_password': hash_password(signup_form.password)}
        user = User(**data)
        session.add(user)
        session.commit()
        return user
