from abc import (
    ABC,
    abstractmethod,
)

from src.db.db import async_session
from src.repositories.scores import ScoresRepository
from src.repositories.students import StudentsRepository


class BaseManager(ABC):
    scores_repo: ScoresRepository
    students_repo: StudentsRepository

    @abstractmethod
    def __init__(self):
        """Initializing the manager"""
        pass

    @abstractmethod
    async def __aenter__(self):
        """Enter the asynchronous context"""
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        """Exit the asynchronous context"""
        pass

    @abstractmethod
    async def commit(self):
        """Commit the transaction"""
        pass

    @abstractmethod
    async def rollback(self):
        """Rollback the transaction"""
        pass


class TransactionManager(BaseManager):
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()
        self.scores_repo = ScoresRepository(self.session)
        self.students_repo = StudentsRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
