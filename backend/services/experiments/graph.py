from polars import DataFrame, col

from backend.schemas.experiments.data import ExperimentDescription, ColumnDetails


async def import_experiment(data: ExperimentDescription) -> dict[str, ColumnDetails]:
    units = await get_all_units()
    result: dict[str, ColumnDetails] = {}

    for column, props in data.headers.ontological_description.columns.items():
        filter_col = 'label' if props.key.endswith('@en') else 'symbol'
        unit_spec = units.filter(col(filter_col) == props.key).to_dict()
        result[column] = ColumnDetails(uri=unit_spec['uri'][0], dimension=unit_spec[DIMENSION_KEY][0])

    pk = data.headers.ontological_description.primary_key
    df = DataFrame(data.body)
    df.columns.remove(pk)
    df.columns.insert(0, pk)
    return result
