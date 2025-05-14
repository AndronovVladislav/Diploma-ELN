import pytest
from fastapi import HTTPException
from sqlalchemy import inspect

from backend.common.enums import ExperimentKind
from backend.models.experiment import (
    Column as SQColumn,
    Measurement as SQMeasurement,
    LaboratoryExperiment,
    ComputationalExperiment,
    ComputationalExperimentTemplate,
    ComputationalExperimentData,
    Schema as SQSchema,
    SchemaKind,
)
from backend.schemas.experiments.data import (
    LaboratoryExperimentDetails,
    ComputationalExperimentDetails,
)
from backend.services.experiments.relational.utils import (
    pivot_measurements,
    to_dict,
    validate_schema,
    construct_lab_experiment_details,
    construct_comp_experiment_details,
)


def test_pivot_measurements_single_row():
    col = SQColumn(
        name='A', ontology='test', ontology_ref='test:001', is_main=False, experiment_id=1
    )
    col.id = 1
    meas = SQMeasurement(row=0, column=1, value='val')
    table = pivot_measurements([meas], [col])
    assert table == [{'A': 'val', 'row': 0}]


def test_to_dict_column():
    col = SQColumn(
        name='B', ontology='ono', ontology_ref='oref', is_main=True, experiment_id=2
    )
    col.id = 2
    d = to_dict(col)
    for attr in inspect(col).mapper.column_attrs:
        assert attr.key in d
    assert d['id'] == 2
    assert d['name'] == 'B'


def test_validate_schema_valid_and_invalid():
    schema = {'x': 1, 'y': 2}
    data_valid = {'x': 'foo', 'y': 'bar'}
    validate_schema(data_valid, schema, SchemaKind.INPUT)

    data_invalid = {'x': 'foo'}
    with pytest.raises(HTTPException) as exc:
        validate_schema(data_invalid, schema, SchemaKind.INPUT)
    assert 'data keys do not match template schema' in str(exc.value)


def test_construct_lab_experiment_details():
    exp = LaboratoryExperiment(
        user_id=1,
        path='/parent/exp1',
        description='desc',
        kind=ExperimentKind.LABORATORY
    )
    exp.id = 10
    col = SQColumn(
        name='C', ontology='ono', ontology_ref='oref', is_main=True, experiment_id=10
    )
    col.id = 1
    meas = SQMeasurement(row=0, column=1, value='v')
    exp.columns = [col]
    exp.measurements = [meas]
    details = construct_lab_experiment_details(exp)
    assert isinstance(details, LaboratoryExperimentDetails)
    assert details.id == 10
    assert details.name == 'exp1'
    assert details.description == 'desc'
    assert details.columns[0].name == 'C'
    assert details.measurements == [{'C': 'v', 'row': 0}]


def test_construct_comp_experiment_details():
    in_schema = SQSchema(type=SchemaKind.INPUT, data={'p': 'val'})
    out_schema = SQSchema(type=SchemaKind.OUTPUT, data={'q': 'val'})
    prm_schema = SQSchema(type=SchemaKind.PARAMETERS, data={'r': 'val'})
    ctx_schema = SQSchema(type=SchemaKind.CONTEXT, data={'s': 'val'})
    in_schema.id, out_schema.id, prm_schema.id, ctx_schema.id = 1, 2, 3, 4

    tmpl = ComputationalExperimentTemplate(
        user_id=1,
        path='/templates/t1',
        input_id=in_schema.id,
        output_id=out_schema.id,
        parameters_id=prm_schema.id,
        context_id=ctx_schema.id
    )
    tmpl.input = in_schema
    tmpl.output = out_schema
    tmpl.parameters = prm_schema
    tmpl.context = ctx_schema
    tmpl.id = 5

    exp = ComputationalExperiment(
        user_id=1,
        template_id=tmpl.id,
        path='/exp2',
        description='desc2',
        kind=ExperimentKind.COMPUTATIONAL
    )
    exp.id = 20
    exp.template = tmpl

    row_model = ComputationalExperimentData(
        row=0,
        experiment_id=20,
        input_id=in_schema.id,
        output_id=out_schema.id,
        parameters_id=prm_schema.id,
        context_id=ctx_schema.id
    )
    row_model.input = in_schema
    row_model.output = out_schema
    row_model.parameters = prm_schema
    row_model.context = ctx_schema
    exp.data = [row_model]

    details = construct_comp_experiment_details(exp)
    assert isinstance(details, ComputationalExperimentDetails)
    assert details.id == 20
    assert details.template.input == {'p': 'val'}
    assert details.data[0].row == 0
    assert details.data[0].input == {'p': 'val'}
