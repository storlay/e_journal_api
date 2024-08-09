import re

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from src.config.config import settings

async_engine = create_async_engine(
    url=settings.db.URL,
    echo=settings.db.ECHO,
    pool_size=settings.db.POOL_SIZE,
    max_overflow=settings.db.MAX_OVERFLOW,
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    id: None

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Converting a class name (CamelCase)
        to a table name (snake_case).
        :return: Table name.
        """
        name = re.sub(
            r"(?<!^)(?=[A-Z])",
            "_",
            cls.__name__,
        ).lower()
        return name

    def to_read_model(self):
        """
        Conversion to a pydantic model.
        :return: Pydantic model.
        """
        pass
