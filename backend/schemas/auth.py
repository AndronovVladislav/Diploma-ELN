from pydantic import BaseModel, Field

from backend.models.user import Role


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserSignup(BaseModel):
    """
    Схема запроса создания нового пользователя.
    """
    username: str
    role: Role = Field(description='Роль')
    password: str = Field(description='Пароль пользователя')

    class Config:
        use_enum_values = True


class UserLogin(BaseModel):
    """
    Схема запроса входа существующего пользователя.
    """
    username: str = Field(description='Электронная почта')
    password: str = Field(description='Пароль пользователя')


class UserUpdate(BaseModel):
    """
    Схема запроса обновления данных существующего пользователя.
    """
    username: str | None = Field(description='Новое имя пользователя')
    password: str | None = Field(description='Новый пароль пользователя')


class UserResponse(BaseModel):
    """
    Схема ответа с данными пользователя клиенту.
    """
    id: int = Field(description='Уникальный идентификатор пользователя')
