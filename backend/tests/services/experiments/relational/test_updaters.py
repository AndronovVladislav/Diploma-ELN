import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import Role
from backend.models import User
from backend.models.utils import connection
from backend.schemas.experiments.requests import (
    ImportLaboratoryExperiment,
    ImportColumn,
    Measurement as ImportMeasurement,
    ImportComputationalTemplate,
    ImportComputationalRow,
    ImportComputationalExperiment,
    UpdateComputationalExperimentRequest,
)
from backend.schemas.experiments.requests import (
    UpdateLaboratoryExperimentRequest,
    Measurement,
)
from backend.services.experiments.relational.creators import (
    import_laboratory_experiment,
    import_computational_experiment,
)
from backend.services.experiments.relational.updaters import (
    update_comp_experiment_data,
    delete_experiment,
)
from backend.services.experiments.relational.updaters import (
    update_lab_experiment_data,
)


@pytest.mark.asyncio
async def test_update_lab_experiment_info(user: User, mocker):
    """
    Должен обновлять path и description лабораторного эксперимента.
    """
    mocker.patch(
        'backend.services.experiments.relational.creators.check_ontologies',
        return_value=None
    )
    mocker.patch(
        'backend.services.experiments.relational.creators.validate_schema',
        return_value=None
    )

    payload = ImportLaboratoryExperiment(
        path='exp_lab_upd',
        description='initial',
        columns=[ImportColumn(name='col1', ontology='ont1', ontology_ref='ref1', is_main=True)],
        measurements=[Measurement(row=0, col1='val1')],
    )
    details = await import_laboratory_experiment(user, payload)

    update_req = UpdateLaboratoryExperimentRequest(path='new_path', description='new_desc')
    updated = await update_lab_experiment_data(details.id, update_req)

    assert updated.name == 'new_path'
    assert updated.description == 'new_desc'


@pytest.mark.asyncio
async def test_update_lab_experiment_columns(user: User, mocker):
    """
    Должен обновлять columns лабораторного эксперимента.
    """
    mocker.patch(
        'backend.services.experiments.relational.creators.check_ontologies',
        return_value=None
    )
    mocker.patch(
        'backend.services.experiments.relational.updaters.check_ontologies',
        return_value=None
    )
    mocker.patch(
        'backend.services.experiments.relational.creators.validate_schema',
        return_value=None
    )

    payload = ImportLaboratoryExperiment(
        path='exp_lab_cols',
        description='desc',
        columns=[ImportColumn(name='col1', ontology='ont1', ontology_ref='ref1', is_main=True)],
        measurements=[Measurement(row=0, col1='val1')],
    )
    details = await import_laboratory_experiment(user, payload)

    new_cols = [ImportColumn(
        name='col1',
        ontology='ont1',
        ontology_ref='ref2',
        is_main=False,
    )]
    update_req = UpdateLaboratoryExperimentRequest(columns=new_cols)
    updated = await update_lab_experiment_data(details.id, update_req)

    assert updated.columns[0].ontology_ref == 'ref2'
    assert updated.columns[0].is_main is False


@pytest.mark.asyncio
async def test_update_lab_experiment_measurements(user: User, mocker):
    """
    Должен обновлять measurements лабораторного эксперимента.
    """
    mocker.patch(
        'backend.services.experiments.relational.creators.check_ontologies',
        return_value=None
    )
    mocker.patch(
        'backend.services.experiments.relational.updaters.check_ontologies',
        return_value=None
    )
    mocker.patch(
        'backend.services.experiments.relational.creators.validate_schema',
        return_value=None
    )

    payload = ImportLaboratoryExperiment(
        path='exp_lab_meas',
        description='desc',
        columns=[ImportColumn(name='col1', ontology='ont1', ontology_ref='ref1', is_main=True)],
        measurements=[Measurement(row=0, col1='val1')],
    )
    details = await import_laboratory_experiment(user, payload)

    new_meas = [Measurement(row=0, col1='val2')]
    update_req = UpdateLaboratoryExperimentRequest(measurements=new_meas)
    updated = await update_lab_experiment_data(details.id, update_req)

    assert any(m.get('col1') == 'val2' for m in updated.measurements)


@pytest.mark.asyncio
async def test_update_comp_experiment_info(user: User, mocker):
    """
    Должен обновлять path и description вычислительного эксперимента.
    """
    mocker.patch(
        'backend.services.experiments.relational.creators.validate_schema',
        return_value=None
    )

    tmpl = ImportComputationalTemplate(
        path='tmpl_upd',
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
        path='exp_comp_upd',
        template=tmpl,
        data=[row],
    )
    comp_details = await import_computational_experiment(user, payload)

    update_req = UpdateComputationalExperimentRequest(path='new_comp', description='new_desc')
    updated = await update_comp_experiment_data(comp_details.id, update_req)

    assert updated.name == 'new_comp'
    assert updated.description == 'new_desc'


@pytest.mark.asyncio
async def test_update_comp_experiment_data_rows(user: User, mocker):
    """
    Должен обновлять data вычислительного эксперимента при передаче нового списка data.
    """
    # пропускаем валидацию схем при обновлении
    mocker.patch(
        'backend.services.experiments.relational.updaters.validate_schema',
        return_value=None
    )
    tmpl = ImportComputationalTemplate(
        path='tmpl_test',
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
        path='exp_comp_test',
        template=tmpl,
        data=[row],
    )
    details = await import_computational_experiment(user, payload)

    # обновляем data: меняем context
    new_data = (
        {'a': 1},
        {'b': 2},
        {'p': 3},
        {'ctx': 'y'},
    )
    update_req = UpdateComputationalExperimentRequest(data=[new_data])
    updated = await update_comp_experiment_data(details.id, update_req)

    assert len(updated.data) == 1
    assert updated.data[0].context == {'ctx': 'y'}


@pytest.mark.asyncio
async def test_delete_experiment_success_and_errors(user: User, mocker):
    """
    Должен удалять эксперимент, выдавать 404 для несуществующего и 403 для чужого.
    """

    mocker.patch(
        'backend.services.experiments.relational.utils.validate_all_ontology_uris_exist',
        return_value=None
    )

    @connection
    async def create_other_user(session: AsyncSession):
        other = User(username='other_user', hashed_password='...', role=Role.RESEARCHER)
        session.add(other)
        return other

    lab_payload = ImportLaboratoryExperiment(
        path='exp_to_delete',
        description='to delete',
        columns=[ImportColumn(name='c', ontology='om2', ontology_ref='r', is_main=True)],
        measurements=[ImportMeasurement(row=0, c='v')],
    )
    lab_details = await import_laboratory_experiment(user, lab_payload)

    resp = await delete_experiment(lab_details.id, user)
    assert resp.status_code == 204

    with pytest.raises(HTTPException) as exc_info:
        await delete_experiment(99999, user)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    lab_details2 = await import_laboratory_experiment(user, lab_payload)
    with pytest.raises(HTTPException) as exc_info:
        await delete_experiment(lab_details2.id, await create_other_user())
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
