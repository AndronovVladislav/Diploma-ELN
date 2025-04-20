from fastapi import APIRouter

from backend.schemas.templates.requests import TemplateCreateRequest, TemplateCreateResponse
from backend.services.templates.templates import create_computational_template as create_computational_template_service

router = APIRouter(prefix='/template', tags=['Computational Experiment Templates'])


@router.post('', response_model=TemplateCreateResponse)
async def create_computational_template(payload: TemplateCreateRequest):
    return await create_computational_template_service(payload)
