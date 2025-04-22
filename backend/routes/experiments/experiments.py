from typing import Any

from fastapi import APIRouter, Query, Depends, Response

from backend.models import User
from backend.routes.auth.validation import get_current_auth_user
from backend.routes.experiments.utils import flat_to_tree
from backend.schemas.experiments.data import LaboratoryExperimentDetails
from backend.schemas.experiments.requests import UpdateLaboratoryExperimentRequest, CreateExperimentRequest
# from backend.services.experiments.graph import import_experiment as import_experiment_service
from backend.services.experiments.relational.creators import create_user_experiment as create_user_experiment_service
from backend.services.experiments.relational.getters import (
    get_user_experiments as get_user_experiments_service,
    get_experiment_data as get_experiment_data_service,
)
from backend.services.experiments.relational.updaters import (
    update_experiment_data as update_experiment_data_service,
    delete_experiment as delete_experiment_service,
)

router = APIRouter(prefix='/experiment', tags=['Experiments'])


@router.get('/', response_model=list[dict])
async def get_user_experiments(user: User = Depends(get_current_auth_user), desired_keys: list[str] = Query()):
    return flat_to_tree(await get_user_experiments_service(user.username), desired_keys)


@router.post('/', response_model=LaboratoryExperimentDetails)
async def create_user_experiment(request: CreateExperimentRequest, user: User = Depends(get_current_auth_user)):
    return await create_user_experiment_service(user, request.path, request.kind)


@router.get('/{experiment_id}', response_model=LaboratoryExperimentDetails | Any)
async def get_experiment_data(experiment_id: int):
    return await get_experiment_data_service(experiment_id)


@router.patch('/{experiment_id}', response_model=LaboratoryExperimentDetails)
async def update_experiment_data(experiment_id: int, update: UpdateLaboratoryExperimentRequest):
    return await update_experiment_data_service(experiment_id, update)


@router.delete('/{experiment_id}', response_class=Response)
async def delete_experiment(experiment_id: int):
    return await delete_experiment_service(experiment_id)

# @router.post('/import')
# async def import_experiment(experiment: ExperimentDescription) -> Any:  # TODO: написать схему
#     return await import_experiment_service(experiment)
