from fastapi import APIRouter, HTTPException

from schemas.users import UserCreate, UserResponse
from services.users import create_user, get_user

router = APIRouter(prefix='/users')

# @router.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     ...


@router.post("/signup")
async def signup(form: UserCreate) -> UserResponse:
    user = await get_user(form.email)
    if not user:
        await create_user(form)
        return UserResponse.model_validate(user, from_attributes=True)
    return HTTPException(400, 'Пользователь с указанным email уже существует!')
