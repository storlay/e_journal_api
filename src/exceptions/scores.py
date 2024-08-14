from fastapi import status

from src.exceptions.base import EJournalException


class ScoreNotFoundException(EJournalException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Score not found"


class IncorrectStudentException(EJournalException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Wrong student ID"


class IncorrectDateOfReceiptException(EJournalException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "The date of receipt of the score cannot be longer than the current date"
