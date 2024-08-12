from fastapi import status

from src.exceptions.base import EJournalException


class StudentNotFoundException(EJournalException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Student not found"
