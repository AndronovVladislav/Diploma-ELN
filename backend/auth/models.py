from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(Enum):
    ADMIN = 'admin'
    ANALYST = 'analyst'
    SCIENTIST = 'scientist'


class UserSignup(BaseModel):
    """
    Схема запроса создания нового пользователя.
    """
    name: str = Field(description='Имя')
    surname: str = Field(description='Фамилия')
    email: EmailStr = Field(description='Электронная почта')
    role: Role = Field(description='Роль')
    password: str = Field(description='Пароль пользователя')

    class Config:
        use_enum_values = True


class UserLogin(BaseModel):
    """
    Схема запроса входа существующего пользователя.
    """
    email: EmailStr = Field(description='Электронная почта')
    password: str = Field(description='Пароль пользователя')


class UserUpdate(BaseModel):
    """
    Схема запроса обновления данных существующего пользователя.
    """
    username: str | None = Field(description='Новое имя пользователя')
    email: EmailStr | None = Field(description='Новая электронная почта пользователя')
    password: str | None = Field(description='Новый пароль пользователя')


class UserResponse(BaseModel):
    """
    Схема ответа с данными пользователя клиенту.
    """
    id: int = Field(description='Уникальный идентификатор пользователя')
