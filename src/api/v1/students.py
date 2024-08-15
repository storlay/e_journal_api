from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.api.dependencies import TransactionDep
from src.api.pagination import (
    BasePaginationResponse,
    PaginationParams,
)
from src.schemas.students import (
    AddStudentSchema,
    StudentIdSchema,
    StudentSchema,
    UpdateStudentSchema,
)
from src.services.students import StudentsService


router = APIRouter(
    tags=["Students"],
    prefix="/students",
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Getting all students",
    description="Getting all students with their scores with pagination.",
)
async def get_all_students(
    transaction: TransactionDep,
    pagination: PaginationParams = Depends(),
) -> BasePaginationResponse[StudentSchema]:
    """
    Getting all students.
    :param transaction: Database transaction.
    :param pagination: Pagination params.
    :return: List of Pydantic models representing the students.
    """
    return await StudentsService.get_all_students(
        transaction,
        pagination,
    )


@router.get(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Getting a student by ID",
    description="Getting a student with their scores by ID.",
)
async def get_student(
    transaction: TransactionDep,
    student_id: int,
) -> StudentSchema:
    """
    Getting a student by ID.
    :param transaction: Database transaction.
    :param student_id: Student ID.
    :return: Pydantic model representing the student.
    """
    return await StudentsService.get_student(
        transaction,
        student_id,
    )


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    summary="Adding a new student",
    description="Adding a new student.",
)
async def add_student(
    transaction: TransactionDep,
    student_data: AddStudentSchema,
) -> StudentIdSchema:
    """
    Adding a new student.
    :param transaction: Database transaction.
    :param student_data: Pydantic model representing student data.
    :return: Pydantic model representing the created student ID.
    """
    return await StudentsService.add_student(
        transaction,
        student_data,
    )


@router.patch(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Updating a student by ID",
    description="Updating a student by ID.",
)
async def update_student(
    transaction: TransactionDep,
    student_data: UpdateStudentSchema,
    student_id: int,
) -> StudentIdSchema:
    """
    Updating a student by ID.
    :param transaction: Database transaction.
    :param student_id: Student ID.
    :param student_data: Pydantic model representing student data.
    :return: Pydantic model representing the updated student ID.
    """
    return await StudentsService.update_student(
        transaction,
        student_id,
        student_data,
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a student by ID",
    description="Deleting a student by ID.",
)
async def delete_student(
    transaction: TransactionDep,
    student_id: int,
) -> None:
    """
    Deleting a student by ID.
    :param transaction: Database transaction.
    :param student_id: Student ID.
    :return: None.
    """
    await StudentsService.delete_student(
        transaction,
        student_id,
    )
