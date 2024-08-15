from fastapi import status

from src.tests.conftest import (
    ScoresFactory,
    StudentsFactory,
)

STUDENT: StudentsFactory = StudentsFactory.build()
SCORE: ScoresFactory = ScoresFactory.build()


PAGINATION_VALIDATION_DATA = [
    (1, 10, status.HTTP_200_OK),
    (2, 1, status.HTTP_200_OK),
    (1, 100_000, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("invalid_page", 1, status.HTTP_422_UNPROCESSABLE_ENTITY),
    (1, "invalid_size", status.HTTP_422_UNPROCESSABLE_ENTITY),
]

DELETE_VALIDATION_DATA = [
    (1, status.HTTP_204_NO_CONTENT),
    (10, status.HTTP_204_NO_CONTENT),
    (100_000, status.HTTP_204_NO_CONTENT),
    ("invalid_id", status.HTTP_422_UNPROCESSABLE_ENTITY),
]
