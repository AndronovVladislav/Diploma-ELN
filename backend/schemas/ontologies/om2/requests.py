from typing import Annotated

from pydantic import BaseModel, Field

from backend.schemas.ontologies.common import SelectOnlyEnglishVersion


class UnitShortDetails(BaseModel):
    label: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]
    dimension: Annotated[str, SelectOnlyEnglishVersion]
    comment: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]
    uri: str
