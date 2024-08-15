from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
)

from src.models.utils import ClassNamesEnum
from src.schemas.scores import ScoresForStudentSchema


class StudentSchema(BaseModel):
    id: int
    class_name: str
    first_name: str
    last_name: str
    age: int
    scores: list[ScoresForStudentSchema]


class AddStudentSchema(BaseModel):
    class_name: ClassNamesEnum
    first_name: Annotated[str, Field(max_length=50)]
    last_name: Annotated[str, Field(max_length=50)]
    age: Annotated[int, Field(ge=7)]


class UpdateStudentSchema(BaseModel):
    class_name: Annotated[
        ClassNamesEnum | None,
        Field(None),
    ]
    first_name: Annotated[
        str | None,
        Field(None, max_length=50),
    ]
    last_name: Annotated[
        str | None,
        Field(None, max_length=50),
    ]
    age: Annotated[
        int | None,
        Field(None, ge=7),
    ]


class StudentIdSchema(BaseModel):
    student_id: int
