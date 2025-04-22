from fastapi import HTTPException, status, Response
from neo4j import AsyncSession as NeoSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import User
from backend.models.experiment import Schema, SchemaKind, ComputationalExperimentTemplate
from backend.models.utils import connection
from backend.ontology.base import connection as neo4j_connection, CypherQueryBuilder, CypherCondition
from backend.schemas.templates.data import TemplateDetails
from backend.schemas.templates.requests import CreateTemplateRequest, UpdateTemplateRequest
from backend.services.experiments.relational.utils import to_dict

builder = CypherQueryBuilder()
TEMPLATE_NOT_FOUND_MESSAGE = 'Шаблон вычислительного эксперимента с таким id не найден'
OTHER_TEMPLATE_UPDATING_MESSAGE = 'Нельзя редактировать чужой шаблон'
OTHER_TEMPLATE_DELETING_MESSAGE = 'Нельзя удалить чужой шаблон'


@neo4j_connection
async def validate_all_ontology_uris_exist(uris: set[str], session: NeoSession) -> None:
    q = (
        builder
        .match('(n)')
        .where(CypherCondition('n.uri IN $uris'))
        .return_('n.uri AS uri')
        .build()
    )
    result = await session.run(q, {'uris': list(uris)})
    found_uris = {row['uri'] async for row in result}
    missing = uris - found_uris
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f'Следующие URI не найдены в онтологиях: {sorted(missing)}'
        )


@connection
async def create_user_template(user: User,
                               payload: CreateTemplateRequest,
                               session: AsyncSession,
                               ) -> TemplateDetails:
    template_input = payload.input.model_dump()
    template_output = payload.output.model_dump()
    template_parameters = payload.parameters.model_dump()
    all_uris = set(template_input.values()) | set(template_output.values()) | set(template_parameters.values())
    await validate_all_ontology_uris_exist(all_uris)

    input_schema = Schema(type=SchemaKind.INPUT, data=template_input)
    output_schema = Schema(type=SchemaKind.OUTPUT, data=template_output)
    parameters_schema = Schema(type=SchemaKind.PARAMETERS, data=template_parameters)
    context_schema = Schema(type=SchemaKind.CONTEXT, data=payload.context)

    session.add_all([input_schema, output_schema, parameters_schema, context_schema])
    await session.flush()

    template = ComputationalExperimentTemplate(
        user_id=user.id,
        path=payload.path,
        input_id=input_schema.id,
        output_id=output_schema.id,
        parameters_id=parameters_schema.id,
        context_id=context_schema.id,
    )

    session.add(template)
    await session.flush()

    return TemplateDetails(
        id=template.id,
        path=template.path,
        input=input_schema.data,
        output=output_schema.data,
        parameters=parameters_schema.data,
        context=context_schema.data
    )


@connection
async def get_user_template(user: User, session: AsyncSession) -> list[dict]:
    q = select(ComputationalExperimentTemplate).where(User.id == user.id)
    result = (await session.execute(q)).scalars().all()
    return [to_dict(template) for template in result]


async def get_template(template_id: int, session: AsyncSession) -> ComputationalExperimentTemplate:
    q = (
        select(ComputationalExperimentTemplate)
        .options(
            selectinload(ComputationalExperimentTemplate.input),
            selectinload(ComputationalExperimentTemplate.output),
            selectinload(ComputationalExperimentTemplate.parameters),
            selectinload(ComputationalExperimentTemplate.context),
            selectinload(ComputationalExperimentTemplate.experiments),
        )
        .where(ComputationalExperimentTemplate.id == template_id)
    )

    template = (await session.execute(q)).scalar_one_or_none()

    if template is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TEMPLATE_NOT_FOUND_MESSAGE)

    return template


@connection
async def get_template_details(template_id: int, session: AsyncSession) -> TemplateDetails:
    template = await get_template(template_id, session)

    return TemplateDetails(
        id=template.id,
        path=template.path,
        input=template.input.data,
        output=template.output.data,
        parameters=template.parameters.data,
        context=template.context.data,
    )


@connection
async def update_user_template(update: UpdateTemplateRequest,
                               template_id: int,
                               user: User,
                               session: AsyncSession,
                               ) -> TemplateDetails:
    template = await get_template(template_id, session)

    if template.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=OTHER_TEMPLATE_UPDATING_MESSAGE)

    update_data = update.model_dump(exclude_unset=True)

    if 'path' in update_data:
        template.path = update_data['path']

    return TemplateDetails(
        id=template.id,
        path=template.path,
        input=template.input.data,
        output=template.output.data,
        parameters=template.parameters.data,
        context=template.context.data,
    )


@connection
async def delete_template(template_id: int, user: User, session: AsyncSession) -> Response:
    template = await get_template(template_id, session)

    if template.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=OTHER_TEMPLATE_DELETING_MESSAGE)

    if not len(template.experiments):
        await session.delete(template)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(
        status_code=status.HTTP_403_FORBIDDEN,
        content='Нельзя удалить шаблон, к которому привязаны эксперименты',
    )
