from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.db.db import Base
from src.db.mixins.pk import IntIdPkMixin
from src.schemas.scores import ScoreSchema


class Scores(Base, IntIdPkMixin):
    """
    Student scores model.
    """

    __table_args__ = (
        CheckConstraint(
            "score >= 2 AND score <= 5",
            name="check_score",
        ),
    )

    score: Mapped[int] = mapped_column(SmallInteger)
    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        )
    )

    student: Mapped["Students"] = relationship(
        "Students",
        back_populates="scores",
    )

    def to_read_model(self) -> ScoreSchema:
        return ScoreSchema(
            id=self.id,
            score=self.score,
            student_id=self.student_id,
        )
