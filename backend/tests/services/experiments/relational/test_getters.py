import pytest
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from backend.models import User, LaboratoryExperiment, ComputationalExperiment
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ComputationalExperimentDetails
from backend.services.experiments.relational.getters import export_experiment_data
from backend.services.experiments.relational.getters import (
    get_experiment_data
)
from backend.services.experiments.relational.utils import ExportType


@pytest.mark.asyncio
async def test_get_lab_experiment_data(lab_experiment: LaboratoryExperiment):
    """
    Должен успешно возвращать данные лабораторного эксперимента.
    """

    details = await get_experiment_data(lab_experiment.id)
    assert details.name == 'lab_exp_1'
    assert details.description == 'Test Lab Experiment'


@pytest.mark.asyncio
async def test_get_lab_experiment_data_not_found():
    """
    Должен возвращать 404 ошибку, если лабораторный эксперимент не существует.
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_experiment_data(99999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Эксперимент с таким id не найден' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_comp_experiment_data(comp_experiment: ComputationalExperiment):
    """
    Должен успешно возвращать данные вычислительного эксперимента.
    """
    details: ComputationalExperimentDetails = await get_experiment_data(comp_experiment.id)

    assert details.name == 'comp_exp_1'
    assert details.description == 'Test Computational Experiment'


@pytest.mark.asyncio
async def test_get_comp_experiment_data_not_found():
    """
    Должен возвращать 404 ошибку, если вычислительный эксперимент не существует.
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_experiment_data(99999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Эксперимент с таким id не найден' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_lab_experiment_data_with_related_data(user: User, lab_experiment: LaboratoryExperiment):
    """
    Проверяет, что при загрузке лабораторного эксперимента данные (например, columns и measurements)
    загружаются правильно через selectinload.
    """
    details: LaboratoryExperimentDetails = await get_experiment_data(lab_experiment.id)

    assert len(details.columns) > 0
    assert len(details.measurements) > 0
    assert details.columns[0].name == 'Temperature'
    assert details.measurements[0]['Temperature'] == '25'


@pytest.mark.asyncio
async def test_get_comp_experiment_data_with_related_data(user: User, comp_experiment: ComputationalExperiment):
    """
    Проверяет, что при загрузке вычислительного эксперимента данные (например, template, data) загружаются
    правильно через selectinload.
    """
    details: ComputationalExperimentDetails = await get_experiment_data(comp_experiment.id)

    assert details.template.input == {'input': 1}
    assert details.template.output == {'output': 2}
    assert details.template.parameters == {'parameters': 3}


@pytest.mark.asyncio
async def test_export_lab_experiment_data(user: User, lab_experiment: LaboratoryExperiment, mocker):
    """
    Должен экспортировать данные лабораторного эксперимента в формате JSON.
    """
    response: StreamingResponse = await export_experiment_data(lab_experiment.id, ExportType.JSON)

    assert isinstance(response, StreamingResponse)

    content = b''.join([x async for x in response.body_iterator])
    assert b'"name":"lab_exp_1"' in content
    assert b'"description":"Test Lab Experiment"' in content
    assert b'"columns":[{"id":1,"name":"Temperature","ontology":"om2","ontology_ref":"degreeCelsius","is_main":false}]' in content


@pytest.mark.asyncio
async def test_export_comp_experiment_data(user: User, comp_experiment: ComputationalExperiment, mocker):
    """
    Должен экспортировать данные вычислительного эксперимента в формате XML.
    """
    response: StreamingResponse = await export_experiment_data(comp_experiment.id, ExportType.XML)

    assert isinstance(response, StreamingResponse)

    content = b''.join([x async for x in response.body_iterator])
    assert b'<name>comp_exp_1</name>' in content
    assert b'<description>Test Computational Experiment</description>' in content


@pytest.mark.asyncio
async def test_export_experiment_data_not_found(user: User):
    """
    Должен возвращать 404 ошибку, если эксперимент не существует.
    """
    with pytest.raises(HTTPException) as exc_info:
        await export_experiment_data(99999, ExportType.JSON)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Эксперимент с таким id не найден' in str(exc_info.value.detail)
