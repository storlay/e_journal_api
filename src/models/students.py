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
        "Students",
        back_populates="student",
    )
