import pytest
from httpx import AsyncClient

from backend.models import User
from backend.models.experiment import LaboratoryExperiment
from backend.routes.experiments.experiments import ExperimentKind


@pytest.mark.asyncio
async def test_get_user_experiments(client: AsyncClient, test_user: User):
    """Тест получения экспериментов пользователя"""
    response = await client.get("/experiment/", params={"username": "test_user", "desired_keys": ["key1", "key2"]})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_experiment_data_invalid_kind(client: AsyncClient):
    """Тест с некорректным типом эксперимента"""
    response = await client.get("/experiment/1", params={"kind": "invalid_kind"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_experiment_data_laboratory(client: AsyncClient, lab_experiment: LaboratoryExperiment):
    """Тест получения данных лабораторного эксперимента"""
    response = await client.get(f"/experiment/{lab_experiment.id}", params={"kind": ExperimentKind.LABORATORY})

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "lab_exp_1"
    assert data["description"] == "Test Lab Experiment"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["columns"][0]["name"] == "Temperature"
    assert data["columns"][0]["ontology_element"] == "degreeCelsius"


@pytest.mark.asyncio
async def test_get_experiment_data_invalid_kind(client: AsyncClient):
    """Тест с некорректным типом эксперимента"""
    response = await client.get("/experiment/1", params={"kind": "invalid_kind"})
    assert response.status_code == 422

# FIXME: переделать импорт экспериментов и тест
# @pytest.mark.asyncio
# async def test_import_experiment(client: AsyncClient):
#     """Тест импорта эксперимента"""
#     payload = {
#         "name": "Test Experiment",
#         "description": "A sample experiment",
#         "columns": [{"name": "Temperature", "unit": "Celsius"}]
#     }
#     response = await client.post("/experiment/import", json=payload)
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
