from pydantic import BaseModel


class ScoreSchema(BaseModel):
    id: int
    score: int
    student_id: int
