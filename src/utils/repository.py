from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import (
    delete,
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession


from src.db.db import Base

SCHEMA = TypeVar(
    "SCHEMA",
    bound=BaseModel,
)
MODEL = TypeVar(
    "MODEL",
    bound=Base,
)


class BaseRepository:
    model: MODEL = None

    def __init__(self, session: AsyncSession):
        """
        Initialization the repository.
        :param session: Database connection session.
        """
        self.session = session

    async def add_one(self, data: dict) -> int:
        """
        Adding an object to the database.
        :param data: Object data.
        :return: ID of the created object.
        """
        statement = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def delete_one(self, obj_id: int) -> None:
        """
        Deleting an object from the database by ID.
        :param obj_id: Object ID.
        :return: None.
        """
        statement = delete(self.model).filter_by(id=obj_id)
        await self.session.execute(statement)

    async def edit_one(self, obj_id: int, data: dict) -> int:
        """
        Updating an object in the database.
        :param obj_id: Object ID.
        :param data: Object data.
        :return: ID of the updated object.
        """
        statement = (
            update(self.model)
            .values(**data)
            .filter_by(id=obj_id)
            .returning(self.model.id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def find_one(self, **filter_by) -> SCHEMA:
        """
        Search for an object by filters in the database.
        :param filter_by: Filters.
        :return: Object model.
        """
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one().to_read_model()

    async def find_all(self) -> list[SCHEMA]:
        """
        Getting all objects from the database.
        :return: List of objects models.
        """
        statement = select(self.model)
        result = await self.session.execute(statement)
        result = [row[0].to_read_model() for row in result.all()]
        return result
