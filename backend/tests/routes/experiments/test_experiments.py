import pytest
from httpx import AsyncClient

from backend.models.experiment import LaboratoryExperiment


@pytest.mark.asyncio
async def test_get_experiments(client: AsyncClient, access_token: str):
    """Тест получения экспериментов пользователя"""
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get("/experiment/",
                                params={"desired_keys": ["key1", "key2"]},
                                headers=headers,
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
