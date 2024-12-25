from sqlalchemy import select

from models import async_session_factory
from models.users import User
from schemas.users import UserCreate


async def get_user(email: str) -> User | None:
    async with async_session_factory() as session:
        q = select(User).filter_by(email=email)
        return (await session.execute(q)).one_or_none()


async def create_user(signup_form: UserCreate) -> User:
    async with async_session_factory() as session:
        user = User(**signup_form)
        session.add(user)
        session.commit()
        return user
