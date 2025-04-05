from enum import StrEnum


class Role(StrEnum):
    ADMIN = 'admin'
    RESEARCHER = 'researcher'


class ExperimentKind(StrEnum):
    LABORATORY = 'Лабораторный'
    COMPUTATIONAL = 'Вычислительный'
