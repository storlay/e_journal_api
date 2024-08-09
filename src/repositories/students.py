from src.models.students import Students
from src.utils.repository import BaseRepository


class StudentsRepository(BaseRepository):
    model = Students
