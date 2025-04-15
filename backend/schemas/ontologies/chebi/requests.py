from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from backend.schemas.ontologies.common import SelectOnlyFirst


class UnitShortDetails(BaseModel):
    label: Annotated[str | None, SelectOnlyFirst, Field(None)]
    comment: Annotated[str | None, SelectOnlyFirst, Field(None, alias='iAO_0000115')]
    uri: str
