from models import async_session_factory
from models.users import User
from schemas.users import UserCreate, UserResponse


async def create_user(signup_form: UserCreate) -> UserResponse:
    async with async_session_factory() as session:
        user = User(**signup_form)
        session.add(user)
        session.commit()
        return UserResponse.model_validate(user, from_attributes=True)
