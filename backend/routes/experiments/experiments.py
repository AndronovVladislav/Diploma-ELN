from typing import Any

from fastapi import APIRouter, Query, HTTPException, status

from backend.routes.experiments.utils import flat_to_tree
from backend.schemas.experiments import ColumnDescription
from backend.schemas.experiments import ExperimentDescription
from backend.services.experiments.graph import import_experiment as import_experiment_service
from backend.services.experiments.relational import (
    get_user_experiments as get_user_experiments_service,
    ExperimentKind,
    get_lab_experiment_data,
)

router = APIRouter(prefix="/experiment", tags=["Experiments"])


@router.get('/')
async def get_user_experiments(username: str, desired_keys: list[str] = Query()) -> list[dict]:
    return flat_to_tree(await get_user_experiments_service(username), desired_keys)


@router.get('/{experiment_id}')
async def get_experiment_data(experiment_id: int, kind: ExperimentKind = Query()) -> Any:
    if kind == ExperimentKind.LABORATORY:
        return await get_lab_experiment_data(experiment_id)
    elif kind == ExperimentKind.COMPUTATIONAL:
        return await ...

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect experiment kind')


@router.post('/import')
async def import_experiment(experiment: ExperimentDescription) -> dict[str, ColumnDescription]:
    return await import_experiment_service(experiment)
