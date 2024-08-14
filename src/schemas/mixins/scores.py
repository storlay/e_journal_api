from datetime import date
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from src.exceptions.scores import IncorrectDateOfReceiptException


class DateOfReceiptMixin(BaseModel):
    date_of_receipt: date

    @field_validator("date_of_receipt")
    @classmethod
    def check_date(cls, value):
        if value > date.today():
            raise IncorrectDateOfReceiptException
        return value


class ScoreMixin(BaseModel):
    score: Annotated[int, Field(ge=2, le=5)]


class StudentIdFieldMixin(BaseModel):
    student_id: Annotated[int, Field(ge=1)]
