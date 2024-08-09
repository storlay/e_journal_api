from pydantic import BaseModel

from src.schemas.scores import ScoresForStudentSchema


class StudentSchema(BaseModel):
    id: int
    class_name: str
    first_name: str
    last_name: str
    age: int
    scores: list[ScoresForStudentSchema]
