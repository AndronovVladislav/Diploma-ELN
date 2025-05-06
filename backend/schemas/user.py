from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.common.enums import ExperimentKind


class ExperimentShortInfo(BaseModel):
    """
    Краткая информация об эксперименте для профиля.
    """
    id: int
    name: str
    kind: ExperimentKind
    updated_at: datetime

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class ProfileResponse(BaseModel):
    """
    Схема ответа с данными профиля пользователя клиенту.
    """
    username: str | None
    name: str | None
    surname: str | None

    registered_at: datetime
    position: str | None
    email: str | None
    last_login: datetime

    experiments: list[ExperimentShortInfo]


class UpdateProfileRequest(BaseModel):
    """
    Схема запроса на изменения профиля пользователя.
    """
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    position: str | None = None
    email: str | None = None

    model_config = ConfigDict(extra='ignore')
