import abc

from backend.config import settings

ONTOLOGIES_MAPPING = {k.lower(): v for k, v in settings.ontologies.model_dump().items()}


class BaseError(Exception, abc.ABC):
    """Базовое исключение для всего приложения."""
    message: str = ''

    def __init__(self, details: dict | None = None):
        self.details = details or {}
        self.message = self.message or self.__class__.__name__
        super().__init__(self.message)

    def __str__(self):
        return f'<{self.__class__.__name__}>: {self.message}; details: {self.details}'

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'details': self.details,
        }


class CypherRelatedError(BaseError, abc.ABC):
    pass


class OntologiesRelatedError(BaseError, abc.ABC):
    pass
