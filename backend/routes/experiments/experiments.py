from fastapi import APIRouter, Query, Depends, Response
from fastapi.responses import StreamingResponse

from backend.models import User
from backend.routes.auth.validation import get_current_auth_user
from backend.routes.experiments.utils import flat_to_tree
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ComputationalExperimentDetails
from backend.schemas.experiments.requests import (
    UpdateLaboratoryExperimentRequest,
    CreateLaboratoryExperimentRequest,
    CreateComputationalExperimentRequest, UpdateComputationalExperimentRequest, ImportLaboratoryExperiment,
    ImportComputationalExperiment
)
from backend.services.experiments.relational.creators import (
    create_lab_experiment as create_lab_experiment_service,
    create_comp_experiment as create_comp_experiment_service,
    import_laboratory_experiment as import_laboratory_experiment_service,
    import_computational_experiment as import_computational_experiment_service
)
from backend.services.experiments.relational.getters import (
    get_experiments as get_experiments_service,
    get_experiment_data as get_experiment_data_service,
    export_experiment_data as export_experiment_data_service,
)
from backend.services.experiments.relational.updaters import (
    update_lab_experiment_data as update_lab_experiment_data_service,
    delete_experiment as delete_experiment_service,
    update_comp_experiment_data as update_comp_experiment_data_service,
)
from backend.services.experiments.relational.utils import ExportType

router = APIRouter(prefix='/experiment', tags=['Experiments'])


@router.get('/', response_model=list[dict])
async def get_experiments(user: User = Depends(get_current_auth_user), desired_keys: list[str] = Query()):
    return flat_to_tree(await get_experiments_service(user.username), desired_keys)


@router.post('/laboratory', response_model=LaboratoryExperimentDetails)
async def create_laboratory_experiment(request: CreateLaboratoryExperimentRequest,
                                       user: User = Depends(get_current_auth_user),
                                       ):
    return await create_lab_experiment_service(user, request.path)


@router.post('/computational', response_model=ComputationalExperimentDetails)
async def create_computational_experiment(request: CreateComputationalExperimentRequest,
                                          user: User = Depends(get_current_auth_user),
                                          ):
    return await create_comp_experiment_service(user, request.path, request.template_id)


@router.get('/{experiment_id}', response_model=LaboratoryExperimentDetails | ComputationalExperimentDetails)
async def get_experiment_data(experiment_id: int):
    return await get_experiment_data_service(experiment_id)


@router.patch('/laboratory/{experiment_id}', response_model=LaboratoryExperimentDetails)
async def update_laboratory_experiment_data(experiment_id: int, update: UpdateLaboratoryExperimentRequest):
    return await update_lab_experiment_data_service(experiment_id, update)


@router.patch('/computational/{experiment_id}', response_model=ComputationalExperimentDetails)
async def update_computational_experiment_data(experiment_id: int, update: UpdateComputationalExperimentRequest):
    return await update_comp_experiment_data_service(experiment_id, update)


@router.delete('/{experiment_id}', response_class=Response)
async def delete_experiment(experiment_id: int, user: User = Depends(get_current_auth_user)):
    return await delete_experiment_service(experiment_id, user)


@router.get('/export/{experiment_id}', response_class=StreamingResponse)
async def export_experiment_data(experiment_id: int, export_type: ExportType):
    return await export_experiment_data_service(experiment_id, export_type)


@router.post('/import/laboratory', response_model=LaboratoryExperimentDetails)
async def import_laboratory_experiment(experiment: ImportLaboratoryExperiment, user: User = Depends(get_current_auth_user)):
    return await import_laboratory_experiment_service(user, experiment)


@router.post('/import/computational', response_model=ComputationalExperimentDetails)
async def import_computational_experiment(experiment: ImportComputationalExperiment, user: User = Depends(get_current_auth_user)):
    return await import_computational_experiment_service(user, experiment)
