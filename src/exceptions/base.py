from fastapi import (
    HTTPException,
    status,
)


class EJournalException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )
