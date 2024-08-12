from datetime import date
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
)


class DateOfReceiptMixin(BaseModel):
    date_of_receipt: Annotated[date, Field(ge=date.today())]


class ScoreMixin(BaseModel):
    score: Annotated[int, Field(ge=2, le=5)]


class StudentIdFieldMixin(BaseModel):
    student_id: Annotated[int, Field(ge=1)]

