from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.students import Students
from src.schemas.students import StudentSchema
from src.utils.repository import BaseRepository


class StudentsRepository(BaseRepository):
    model = Students

    async def find_all(self) -> list[StudentSchema]:
        """
        Getting all students from the database.
        :return: List of Pydantic models representing the students.
        """
        statement = (
            select(self.model)
            .options(
                selectinload(self.model.scores)
            )
        )
        result = await self.session.execute(statement)
        result = [row[0].to_read_model() for row in result.all()]
        return result

    async def find_one(self, **filter_by) -> StudentSchema:
        """
        Search for a student by filters in the database.
        :param filter_by: Filters.
        :return: Pydantic models representing the students.
        """
        statement = (
            select(self.model)
            .options(selectinload(self.model.scores))
            .filter_by(**filter_by))
        result = await self.session.execute(statement)
        return result.scalar_one().to_read_model()
