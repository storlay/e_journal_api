from fastapi import status

from src.exceptions.base import EJournalException


class PageNotFoundException(EJournalException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Page not found"
