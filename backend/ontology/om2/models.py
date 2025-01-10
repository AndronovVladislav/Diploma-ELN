from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field

ENG_LANGTAG = '@en'


def select_only_english_version(v) -> str:
    """
    Выбирает из списка одинаковых строк на разных языках только англоязычную версию, используйте с умом.
    """
    if isinstance(v, list):
        for elem in v:
            if isinstance(elem, str) and elem.endswith(ENG_LANGTAG):
                return elem


def select_only_first(v) -> Any:
    if isinstance(v, list) and len(v) > 0:
        return v[0]


SelectOnlyEnglishVersion = BeforeValidator(select_only_english_version)
SelectOnlyFirst = BeforeValidator(select_only_first)


class Unit(BaseModel):
    comment: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]
    uri: str

    symbol: Annotated[str | None, SelectOnlyFirst, Field(None)]
    alternative_symbol: list[str] | None = Field(None, alias='alternativeSymbol')

    label: Annotated[str | None, SelectOnlyEnglishVersion, Field(None)]
    alternative_label: Annotated[str | None, SelectOnlyEnglishVersion, Field(None, alias='alternativeLabel')]

    latex_command: Annotated[str | None, SelectOnlyFirst, Field(None, alias='laTeXCommand')]
    long_comment: Annotated[str | None, SelectOnlyEnglishVersion, Field(None, alias='longcomment')]
    unofficial_abbreviation: list[str] | None = Field(None, alias='unofficialAbbreviation')

    has_factor: Annotated[float | None, SelectOnlyFirst, Field(None, alias='hasFactor')]
    has_exponent: Annotated[float | None, SelectOnlyFirst, Field(None, alias='hasExponent')]


class UnitWithDimension(Unit):
    dimension: Annotated[str, SelectOnlyEnglishVersion]