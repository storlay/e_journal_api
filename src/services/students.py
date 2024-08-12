from sqlalchemy.exc import NoResultFound

from src.api.pagination import (
    BasePaginationResponse,
    PaginationParams,
    Paginator,
)
from src.exceptions.students import StudentNotFoundException
from src.schemas.students import (
    AddStudentSchema,
    StudentIdSchema,
    StudentSchema,
    UpdateStudentSchema,
)
from src.utils.transaction import BaseManager


class StudentsService:
    @staticmethod
    async def get_all_students(
        transaction: BaseManager,
        pagination: PaginationParams,
    ) -> BasePaginationResponse[StudentSchema]:
        """
        The logic of getting all students.
        :param transaction: Database transaction.
        :param pagination: Pagination params.
        :return: List of Pydantic models representing the students.
        """
        async with transaction:
            students = await transaction.students_repo.find_all()
            paginator = Paginator(
                pages=students,
                params=pagination,
            )
            return paginator.get_response()

    @staticmethod
    async def get_student(
        transaction: BaseManager,
        student_id: int,
    ) -> StudentSchema:
        """
        The logic of getting a student by ID.
        :param transaction: Database transaction.
        :param student_id: Student ID
        :return: Pydantic model representing the student.
        """
        async with transaction:
            try:
                student = await transaction.students_repo.find_one(
                    id=student_id,
                )
                return student
            except NoResultFound:
                raise StudentNotFoundException

    @staticmethod
    async def add_student(
        transaction: BaseManager,
        student_data: AddStudentSchema,
    ) -> StudentIdSchema:
        """
        The logic of creating a student.
        :param transaction: Database transaction.
        :param student_data: Pydantic model representing student data.
        :return: Pydantic model representing the created student ID.
        """
        student_data_dict = student_data.model_dump()
        async with transaction:
            student_id = await transaction.students_repo.add_one(
                student_data_dict,
            )
            await transaction.commit()
            return StudentIdSchema(student_id=student_id)

    @staticmethod
    async def update_student(
        transaction: BaseManager,
        student_id: int,
        student_data: UpdateStudentSchema,
    ) -> StudentIdSchema:
        """
        The logic of updating a student by ID.
        :param transaction: Database transaction.
        :param student_id: Student ID.
        :param student_data: Pydantic model representing student data.
        :return: Pydantic model representing the updated student ID.
        """
        student_data_dict = student_data.model_dump(exclude_none=True)
        if student_data_dict:
            async with transaction:
                try:
                    await transaction.students_repo.edit_one(
                        student_id,
                        student_data_dict,
                    )
                    await transaction.commit()
                except NoResultFound:
                    raise StudentNotFoundException
        return StudentIdSchema(student_id=student_id)

    @staticmethod
    async def delete_student(
        transaction: BaseManager,
        student_id: int,
    ) -> None:
        """
        The logic of deleting a student by ID.
        :param transaction: Database transaction.
        :param student_id: Student ID
        :return: None.
        """
        async with transaction:
            await transaction.students_repo.delete_one(
                student_id,
            )
            await transaction.commit()
