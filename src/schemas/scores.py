from datetime import date

from pydantic import BaseModel

from src.schemas.mixins.scores import (
    DateOfReceiptMixin,
    ScoreMixin,
    StudentIdFieldMixin,
)


class ScoreSchema(BaseModel):
    id: int
    score: int
    date_of_receipt: date
    student_id: int


class AddScoreSchema(
    DateOfReceiptMixin,
    ScoreMixin,
    StudentIdFieldMixin,
):
    pass


class UpdateScoreSchema(
    ScoreMixin,
):
    pass


class ScoresForStudentSchema(BaseModel):
    score: int
    date_of_receipt: date


class ScoreIdSchema(BaseModel):
    score_id: int
