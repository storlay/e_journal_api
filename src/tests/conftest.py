from datetime import (
    date,
    timedelta,
)

import factory
import pytest

from src.config.config import settings
from src.db.db import (
    async_engine,
    async_session,
    Base,
)
from src.models.scores import Scores
from src.models.students import Students
from src.models.utils import ClassNamesEnum
from src.utils.transaction import TransactionManager
from src.tests.utils import factory_to_dict


class StudentsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Creating a student with random data.
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
        min_value=8,
        max_value=25,
    )

    class Meta:
        model = Students
        sqlalchemy_session = async_session()


class ScoresFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Creating a score with random data.
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
    student = factory.SubFactory(StudentsFactory)

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
        for _ in range(10):
            score: ScoresFactory = ScoresFactory.build()
            student_data = factory_to_dict(score.student)
            student_id = await transaction.students_repo.add_one(student_data)
            score_data = factory_to_dict(score)
            score_data["student_id"] = student_id
            await transaction.scores_repo.add_one(score_data)
        await transaction.commit()
