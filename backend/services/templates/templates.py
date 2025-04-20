from fastapi import HTTPException
from neo4j import AsyncSession as NeoSession
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.experiment import Schema, SchemaKind, ComputationalExperimentTemplate
from backend.models.utils import connection
from backend.ontology.base import connection as neo4j_connection, CypherQueryBuilder, CypherCondition
from backend.schemas.templates.requests import TemplateCreateResponse, TemplateCreateRequest

builder = CypherQueryBuilder()


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
async def create_computational_template(payload: TemplateCreateRequest,
                                        session: AsyncSession,
                                        ) -> TemplateCreateResponse:
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
        path=payload.path,
        input_id=input_schema.id,
        output_id=output_schema.id,
        parameters_id=parameters_schema.id,
        context_id=context_schema.id,
    )

    session.add(template)
    await session.flush()

    return TemplateCreateResponse(
        id=template.id,
        input_id=input_schema.id,
        output_id=output_schema.id,
        parameters_id=parameters_schema.id,
        context_id=context_schema.id
    )
