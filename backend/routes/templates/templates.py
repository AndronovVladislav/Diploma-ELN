from fastapi import APIRouter, Depends, Response

from backend.models import User
from backend.routes.auth.validation import get_current_auth_user
from backend.routes.experiments.utils import flat_to_tree
from backend.schemas.templates.data import TemplateDetails
from backend.schemas.templates.requests import CreateTemplateRequest, UpdateTemplateRequest
from backend.services.templates.templates import (
    create_template as create_template_service,
    get_templates as get_templates_service,
    get_template_details as get_template_details_service,
    update_template as update_template_service,
    delete_template as delete_template_service,
)

router = APIRouter(prefix='/template', tags=['Computational Experiment Templates'])


@router.get('/', response_model=list[dict])
async def get_templates(user: User = Depends(get_current_auth_user)):
    return flat_to_tree(await get_templates_service(user), ['id'])


@router.get('/{template_id}', response_model=TemplateDetails)
async def get_template_details(template_id: int):
    return await get_template_details_service(template_id)


@router.post('/', response_model=TemplateDetails)
async def create_template(payload: CreateTemplateRequest, user: User = Depends(get_current_auth_user)):
    return await create_template_service(user, payload)


@router.patch('/{template_id}', response_model=TemplateDetails)
async def update_template(payload: UpdateTemplateRequest,
                               template_id: int,
                               user: User = Depends(get_current_auth_user),
                               ):
    return await update_template_service(payload, template_id, user)


@router.delete('/{template_id}', response_class=Response)
async def delete_template(template_id: int, user: User = Depends(get_current_auth_user)):
    return await delete_template_service(template_id, user)
