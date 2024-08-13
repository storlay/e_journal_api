import asyncio
from datetime import (
    date,
    timedelta,
)

import factory
import pytest
from httpx import AsyncClient

from src.config.config import settings
from src.db.db import (
    async_engine,
    async_session,
    Base,
)
from src.main import app
from src.models.scores import Scores
from src.models.students import Students
from src.models.utils import ClassNamesEnum
from src.tests.utils import factory_to_dict
from src.utils.transaction import TransactionManager


class StudentsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Creating a student with random data
    """

    class_name = factory.Faker(
        "enum",
        enum_cls=ClassNamesEnum,
    )
    first_name = factory.Faker(
        "first_name_nonbinary",
    )
    last_name = factory.Faker(
        "last_name_nonbinary",
    )
    age = factory.Faker(
        "pyint",
        min_value=7,
        max_value=25,
    )

    class Meta:
        model = Students
        sqlalchemy_session = async_session()


class ScoresFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Creating a score with random data
    """

    score = factory.Faker(
        "pyint",
        min_value=2,
        max_value=5,
    )
    date_of_receipt = factory.Faker(
        "date_between",
        start_date=date.today() - timedelta(days=180),
    )
    student_id = factory.SelfAttribute(
        "student_id",
    )

    class Meta:
        model = Scores
        sqlalchemy_session = async_session()


@pytest.fixture(
    scope="session",
    autouse=True,
)
async def prepare_database():
    """
    Preparing a test database.
    """
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TransactionManager() as transaction:
        student = StudentsFactory()
        student_dict = factory_to_dict(student)
        student_id = await transaction.students_repo.add_one(student_dict)

        score = ScoresFactory(student_id=student_id)
        score_dict = factory_to_dict(score)
        await transaction.scores_repo.add_one(score_dict)

        await transaction.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Create an instance
    of the default event loop
    for each test case
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    """
    Async client for testing endpoints
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
