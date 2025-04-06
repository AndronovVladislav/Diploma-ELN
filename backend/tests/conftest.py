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
from backend.models.experiment import LaboratoryExperiment, Column, Measurement, Ontology
from backend.models.utils import connection
from backend.models.utils import db_helper
from backend.routes.auth.utils import hash_password

engine = create_async_engine(
    url=settings.db.url,
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
async def ontology() -> Ontology:
    """Создаёт онтологию в БД перед тестом"""

    @connection
    async def create_ontology(session: AsyncSession) -> Ontology:
        ontology = Ontology(name='OM2', label='...')
        session.add(ontology)

        return ontology

    return await create_ontology()


@pytest.fixture
async def lab_experiment(user: User, ontology: Ontology) -> LaboratoryExperiment:
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
            ontology_element='degreeCelsius',
            experiment_id=experiment.id,
            ontology_id=ontology.id,
        )
        session.add(column)
        await session.flush()

        measurement = Measurement(row=1, column=column.id, value='25', experiment_id=experiment.id)
        session.add(measurement)

        return experiment

    return await create_lab_experiment()
