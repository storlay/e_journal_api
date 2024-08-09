from pydantic import BaseModel

from src.schemas.scores import ScoreSchema


class StudentSchema(BaseModel):
    id: int
    class_name: str
    first_name: str
    last_name: str
    age: int
    scores: list[ScoreSchema]
