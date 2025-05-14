from datetime import timedelta
from typing import AsyncIterator

import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.common.enums import Role, ExperimentKind
from backend.config import settings
from backend.main import app
from backend.models import User
from backend.models.experiment import (
    LaboratoryExperiment,
    Column,
    Measurement,
    ComputationalExperiment,
    Schema,
    SchemaKind,
    ComputationalExperimentTemplate,
)
from backend.models.utils import connection
from backend.models.utils import db_helper
from backend.routes.auth.utils import hash_password, create_jwt, TokenType

engine = create_async_engine(
    url=settings.db.url.get_secret_value(),
    echo=True,
    echo_pool=True,
    poolclass=NullPool,
)


@pytest.fixture(scope='session')
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture(autouse=True)
async def override_db_helper():
    """Подменяет сессию в db_helper, чтобы тесты работали корректно."""
    db_helper.session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    yield

    @connection
    async def truncate_all_tables(session: AsyncSession) -> None:
        await session.execute(text('''
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                SET session_replication_role = 'replica';
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                END LOOP;
                SET session_replication_role = 'origin';
            END $$;
        '''))

    await truncate_all_tables()


@pytest.fixture
async def user() -> User:
    """Создаёт тестового пользователя в БД перед тестом"""

    @connection
    async def create_user(session: AsyncSession) -> User:
        user = User(
            username='test_user',
            hashed_password=hash_password('test_password'),
            role=Role.ADMIN,
        )
        session.add(user)
        return user

    return await create_user()


@pytest.fixture
def access_token(user: User) -> str:
    """Создаёт валидный access-токен"""
    return create_jwt(user.username, TokenType.ACCESS, timedelta(minutes=1))


@pytest.fixture
def refresh_token(user: User) -> str:
    """Создаёт валидный refresh-токен"""
    return create_jwt(user.username, TokenType.REFRESH, timedelta(minutes=5))


@pytest.fixture
async def lab_experiment(user: User) -> LaboratoryExperiment:
    """Создаёт лабораторный эксперимент в БД перед тестом"""

    @connection
    async def create_lab_experiment(session: AsyncSession) -> LaboratoryExperiment:
        experiment = LaboratoryExperiment(
            user_id=user.id,
            path=f'/experiments/{user.username}/lab_exp_1',
            description='Test Lab Experiment',
        )
        session.add(experiment)
        await session.flush()

        column = Column(
            name='Temperature',
            ontology_ref='degreeCelsius',
            experiment_id=experiment.id,
            ontology='OM2',
        )
        session.add(column)
        await session.flush()

        measurement = Measurement(row=1, column=column.id, value='25', experiment_id=experiment.id)
        session.add(measurement)

        return experiment

    return await create_lab_experiment()


@pytest.fixture
async def comp_experiment(user: User) -> ComputationalExperiment:
    """Создаёт вычислительный эксперимент в БД перед тестом"""

    @connection
    async def create_comp_experiment(session: AsyncSession) -> ComputationalExperiment:
        input_schema = Schema(type=SchemaKind.INPUT, data={'input': 1})
        output_schema = Schema(type=SchemaKind.OUTPUT, data={'output': 2})
        params_schema = Schema(type=SchemaKind.PARAMETERS, data={'parameters': 3})
        context_schema = Schema(type=SchemaKind.CONTEXT, data={'context': 4})
        session.add_all([input_schema, output_schema, params_schema, context_schema])
        await session.flush()

        comp_template = ComputationalExperimentTemplate(
            user_id=user.id,
            path='/tests/template_1',
            input_id=input_schema.id,
            output_id=output_schema.id,
            parameters_id=params_schema.id,
            context_id=context_schema.id,
        )
        session.add(comp_template)
        await session.flush()

        experiment = ComputationalExperiment(
            user_id=user.id,
            template_id=comp_template.id,
            path='/tests/comp_exp_1',
            description='Test Computational Experiment',
            kind=ExperimentKind.COMPUTATIONAL,
        )
        session.add(experiment)
        await session.flush()

        return experiment

    return await create_comp_experiment()
