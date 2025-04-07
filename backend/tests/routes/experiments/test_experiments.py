import pytest
from httpx import AsyncClient

from backend.models import User
from backend.models.experiment import LaboratoryExperiment


@pytest.mark.asyncio
async def test_get_user_experiments(client: AsyncClient, user: User):
    """Тест получения экспериментов пользователя"""
    response = await client.get("/experiment/",
                                params={"username": user.username, "desired_keys": ["key1", "key2"]},
                                )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_experiment_data_laboratory(client: AsyncClient, lab_experiment: LaboratoryExperiment):
    """Тест получения данных лабораторного эксперимента"""
    response = await client.get(f"/experiment/{lab_experiment.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "lab_exp_1"
    assert data["description"] == "Test Lab Experiment"
    assert isinstance(data["measurements"], list)
    assert len(data["measurements"]) > 0
    assert data["columns"][0]["name"] == "Temperature"
    assert data["columns"][0]["ontology_ref"] == "degreeCelsius"

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
