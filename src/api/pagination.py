from typing import (
    Generic,
    TypeVar,
)
from fastapi import Query
from pydantic import BaseModel

from src.exceptions.pagination import PageNotFoundException

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Query(
        1,
        ge=1,
        description="Page number",
    )
    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Page size",
    )


class BasePaginationResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


class Paginator(Generic[T]):
    def __init__(
        self,
        pages: list[T],
        params: PaginationParams,
    ):
        self.pages = pages
        self.params = params

    def paginate(self) -> list[T]:
        start = (self.params.page - 1) * self.params.size
        end = start + self.params.size
        return self.pages[start:end]

    def get_response(self) -> BasePaginationResponse:
        items_quantity = len(self.pages)
        pages_quantity = items_quantity // self.params.size + bool(
            items_quantity % self.params.size
        )
        if self.params.page > pages_quantity != 0:
            raise PageNotFoundException
        return BasePaginationResponse[T](
            items=self.paginate(),
            total=items_quantity,
            page=self.params.page,
            size=self.params.size,
            pages=pages_quantity,
        )
