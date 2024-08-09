from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    Enum as SQLAEnum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.db.db import Base
from src.db.mixins.pk import IntIdPkMixin
from src.schemas.scores import (
    ScoreSchema,
    ScoresForStudentSchema,
)
from src.schemas.students import StudentSchema


class ClassNamesEnum(Enum):
    MATH: str = "Math"
    SCIENCE: str = "Science"
    ART: str = "Art"


class Students(Base, IntIdPkMixin):
    """
    Student model.
    """

    __table_args__ = (
        CheckConstraint(
            "age > 7",
            name="check_age",
        ),
        CheckConstraint(
            "length(first_name) <= 50",
            name="first_name_len",
        ),
        CheckConstraint(
            "length(last_name) <= 50",
            name="last_name_len",
        ),
    )

    class_name: Mapped[ClassNamesEnum] = mapped_column(
        SQLAEnum(ClassNamesEnum),
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int]

    scores: Mapped[list["Scores"]] = relationship(
        "Scores",
        back_populates="student",
    )

    def to_read_model(self) -> StudentSchema:
        return StudentSchema(
            id=self.id,
            class_name=self.class_name,
            first_name=self.first_name,
            last_name=self.last_name,
            age=self.age,
            scores=self.get_scores(),
        )

    def get_scores(self) -> list[ScoresForStudentSchema]:
        scores = []
        for score in self.scores:  # type: ScoreSchema
            score_info = ScoresForStudentSchema(
                score=score.score,
                date_of_receipt=score.date_of_receipt,
            )
            scores.append(score_info)
        return scores
