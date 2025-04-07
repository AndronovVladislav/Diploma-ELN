from backend.base import ONTOLOGIES_MAPPING


def get_ontologies_names() -> list[str]:
    return list(ONTOLOGIES_MAPPING.keys())
