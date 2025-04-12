from typing import Any

from pydantic import BeforeValidator

ENG_LANGTAG = '@en'


def select_only_english_version(v) -> str | None:
    """
    Выбирает из списка строк на разных языках только англоязычную версию, используйте с умом.
    """
    if isinstance(v, list):
        for elem in v:
            if isinstance(elem, str) and elem.endswith(ENG_LANGTAG):
                return elem.removesuffix(ENG_LANGTAG)
    return None


def select_only_first(v) -> Any:
    if isinstance(v, list) and len(v) > 0:
        return v[0]
    return None


SelectOnlyEnglishVersion = BeforeValidator(select_only_english_version)
SelectOnlyFirst = BeforeValidator(select_only_first)
