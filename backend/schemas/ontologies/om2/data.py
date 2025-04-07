from typing import Annotated

from pydantic import BaseModel, Field

from backend.schemas.ontologies.om2.common import SelectOnlyEnglishVersion, SelectOnlyFirst


class Unit(BaseModel):
    comment: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]
    uri: str

    symbol: Annotated[str | None, SelectOnlyFirst, Field(None)]
    dimension: Annotated[str, SelectOnlyEnglishVersion]
    label: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]

    alternative_symbol: list[str] | None = Field(None, alias='alternativeSymbol')
    alternative_label: Annotated[str | None, SelectOnlyEnglishVersion, Field(None, alias='alternativeLabel')]

    latex_command: Annotated[str | None, SelectOnlyFirst, Field(None, alias='laTeXCommand')]
    long_comment: Annotated[str | None, SelectOnlyEnglishVersion, Field(None, alias='longcomment')]
    unofficial_abbreviation: list[str] | None = Field(None, alias='unofficialAbbreviation')

    has_factor: Annotated[float | None, SelectOnlyFirst, Field(None, alias='hasFactor')]
    has_exponent: Annotated[float | None, SelectOnlyFirst, Field(None, alias='hasExponent')]
