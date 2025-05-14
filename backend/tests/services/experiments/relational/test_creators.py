import pytest

from backend.models import User
from backend.schemas.experiments.requests import (
    ImportLaboratoryExperiment,
    ImportComputationalExperiment,
    ImportColumn,
    Measurement,
    ImportComputationalTemplate,
    ImportComputationalRow,
)
from backend.services.experiments.relational.creators import (
    import_laboratory_experiment,
    import_computational_experiment,
)


@pytest.mark.asyncio
async def test_import_laboratory_experiment_integration(user: User, mocker):
    """
    Должен создать лабораторный эксперимент с одной колонкой и одним измерением.
    """
    payload = ImportLaboratoryExperiment(
        path='exp_lab',
        description='Lab experiment',
        columns=[ImportColumn(name='col1', ontology='om2', ontology_ref='ref1', is_main=True)],
        measurements=[Measurement(row=0, col1='val1')],
    )
    mocker.patch(
        'backend.services.experiments.relational.utils.validate_all_ontology_uris_exist',
        return_value=None
    )
    details = await import_laboratory_experiment(user, payload)
    assert details.name == 'exp_lab'
    assert details.description == 'Lab experiment'
    assert len(details.columns) == 1
    assert details.columns[0].name == 'col1'
    assert len(details.measurements) == 1
    assert details.measurements[0]['col1'] == 'val1'


@pytest.mark.asyncio
async def test_import_computational_experiment_integration(user: User):
    """
    Должен создать вычислительный эксперимент с шаблоном и одной строкой данных.
    """
    template = ImportComputationalTemplate(
        path='tmpl1',
        input={'a': 1},
        output={'b': 2},
        parameters={'p': 3},
        context={'ctx': 'x'},
    )
    row = ImportComputationalRow(
        input={'a': 1},
        output={'b': 2},
        parameters={'p': 3},
        context={'ctx': 'x'},
    )
    payload = ImportComputationalExperiment(
        path='exp_comp',
        template=template,
        data=[row],
    )
    details = await import_computational_experiment(user, payload)
    assert details.name == 'exp_comp'
    assert len(details.data) == 1
    assert details.data[0].input == {'a': 1}
