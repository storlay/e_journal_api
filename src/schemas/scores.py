from datetime import date

from pydantic import BaseModel


class ScoreSchema(BaseModel):
    id: int
    score: int
    date_of_receipt: date
    student_id: int


class ScoresForStudentSchema(BaseModel):
    score: int
    date_of_receipt: date
