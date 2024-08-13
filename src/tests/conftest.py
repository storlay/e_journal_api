from datetime import (
    date,
    timedelta,
)

import factory

from src.db.db import (
    async_session,
)
from src.models.scores import Scores
from src.models.students import Students
from src.models.utils import ClassNamesEnum


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
