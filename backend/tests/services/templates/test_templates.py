import pytest
from fastapi import HTTPException, status

from backend.models import User
from backend.schemas.templates.requests import CreateTemplateRequest, UpdateTemplateRequest, TemplateSchemaData
from backend.services.templates.templates import (
    create_template,
    update_template,
    get_template_details, delete_template,
)


@pytest.fixture(autouse=True)
async def mock_neo4j_requests(mocker):
    mocker.patch(
        'backend.services.templates.templates.validate_all_ontology_uris_exist',
        return_value=None
    )


@pytest.mark.asyncio
async def test_create_template(user: User):
    """
    Должен успешно создавать новый шаблон вычислительного эксперимента.
    """
    template_data = CreateTemplateRequest(
        path='template_1',
        input=TemplateSchemaData(input_param='om2:...'),
        output=TemplateSchemaData(output_param='om2:...'),
        parameters=TemplateSchemaData(param='om2:...'),
        context={'ctx': 'x'},
    )
    template = await create_template(user, template_data)

    assert template.path == 'template_1'
    assert template.input == {'input_param': 'om2:...'}
    assert template.output == {'output_param': 'om2:...'}
    assert template.parameters == {'param': 'om2:...'}
    assert template.context == {'ctx': 'x'}


@pytest.mark.asyncio
async def test_create_template_duplicate_path(user: User):
    """
    Должен возвращать ошибку 400, если шаблон с таким path уже существует.
    """
    template_data = CreateTemplateRequest(
        path='template_1',
        input=TemplateSchemaData(input_param='om2:...'),
        output=TemplateSchemaData(output_param='om2:...'),
        parameters=TemplateSchemaData(param='om2:...'),
        context={'ctx': 'x'},
    )
    await create_template(user, template_data)

    with pytest.raises(HTTPException) as exc_info:
        await create_template(user, template_data)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Шаблон вычислительного эксперимента с таким путём уже существует' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_update_template(user: User):
    """
    Должен успешно обновить данные шаблона.
    """
    template_data = CreateTemplateRequest(
        path='template_1',
        input=TemplateSchemaData(input_param='om2:...'),
        output=TemplateSchemaData(output_param='om2:...'),
        parameters=TemplateSchemaData(param='om2:...'),
        context={'ctx': 'x'},
    )
    template = await create_template(user, template_data)

    updated_data = UpdateTemplateRequest(path='template_2')
    updated_template = await update_template(updated_data, template.id, user)

    assert updated_template.path == 'template_2'


@pytest.mark.asyncio
async def test_get_template(user: User):
    """
    Должен успешно вернуть шаблон по его ID.
    """
    template_data = CreateTemplateRequest(
        path='template_1',
        input=TemplateSchemaData(input_param='om2:...'),
        output=TemplateSchemaData(output_param='om2:...'),
        parameters=TemplateSchemaData(param='om2:...'),
        context={'ctx': 'x'},
    )
    template = await create_template(user, template_data)

    fetched_template = await get_template_details(template.id)

    assert fetched_template.path == 'template_1'
    assert fetched_template.input == {'input_param': 'om2:...'}
    assert fetched_template.output == {'output_param': 'om2:...'}
    assert fetched_template.parameters == {'param': 'om2:...'}
    assert fetched_template.context == {'ctx': 'x'}


@pytest.mark.asyncio
async def test_get_template_not_found():
    """
    Должен возвращать 404 ошибку, если шаблон с таким ID не существует.
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_template_details(99999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Шаблон вычислительного эксперимента с таким id не найден' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_delete_template(user: User):
    """
    Должен успешно удалить шаблон.
    """
    template_data = CreateTemplateRequest(
        path="template_to_delete",
        input=TemplateSchemaData(input_param='om2:...'),
        output=TemplateSchemaData(output_param='om2:...'),
        parameters=TemplateSchemaData(param='om2:...'),
        context={"ctx": "x"},
    )
    template = await create_template(user, template_data)

    await delete_template(template.id, user)

    with pytest.raises(HTTPException) as exc_info:
        await get_template_details(template.id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Шаблон вычислительного эксперимента с таким id не найден' in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_delete_template_not_found(user: User):
    """
    Должен возвращать 404 ошибку, если шаблон с таким ID не существует.
    """
    with pytest.raises(HTTPException) as exc_info:
        await delete_template(99999, user)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert 'Шаблон вычислительного эксперимента с таким id не найден' in str(exc_info.value.detail)


# @pytest.mark.asyncio
# async def test_delete_template_permission_error(user: User):
#     """
#     Должен возвращать 403 ошибку, если пользователь не имеет прав на удаление шаблона.
#     """
#     # Создаем шаблон
#     template_data = CreateTemplateRequest(
#         path="template_for_permission_check",
#         input={"input_param": 1},
#         output={"output_param": 2},
#         parameters={"param": 3},
#         context={"ctx": "x"},
#     )
#     template = await create_template(user, template_data, session)
#
#     # Создаем другого пользователя
#     other_user = User(username="other_user")
#     session.add(other_user)
#     await session.flush()
#
#     # Попытка другого пользователя удалить шаблон
#     with pytest.raises(HTTPException) as excinfo:
#         await delete_template(template.id, other_user, session)
#
#     assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
#     assert 'У вас нет прав для удаления этого шаблона' in str(excinfo.value.detail)
