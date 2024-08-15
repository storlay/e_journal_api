from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient

from src.tests.api_tests.v1_tests.conftest import BASE_API_URL
from src.tests.api_tests.v1_tests.unit_tests.conftest import (
    DELETE_VALIDATION_DATA,
    PAGINATION_VALIDATION_DATA,
    STUDENT,
)


@pytest.mark.parametrize(
    "class_name, first_name, last_name, age, status_code",
    [
        (
            "invalid_class_name",
            STUDENT.first_name,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            STUDENT.class_name.value,
            "too_long_first_name" * 8,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            STUDENT.class_name.value,
            STUDENT.first_name,
            "too_long_last_name" * 8,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            STUDENT.class_name.value,
            STUDENT.first_name,
            STUDENT.last_name,
            1,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            STUDENT.class_name.value,
            STUDENT.first_name,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_201_CREATED,
        ),
    ],
)
async def test_add_student(
    class_name: str | Any,
    first_name: str | Any,
    last_name: str | Any,
    age: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the adding a student.
    :param class_name: Student's class type.
    :param first_name: Student's first name
    :param last_name: Student's last name.
    :param age: Student's age.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.post(
        BASE_API_URL + "/students/add",
        json={
            "class_name": class_name,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
        },
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert len(response_data) == 1
        assert "student_id" in response_data


@pytest.mark.parametrize(
    "student_id, status_code",
    [
        (2, status.HTTP_200_OK),
        (4, status.HTTP_200_OK),
        (100_000, status.HTTP_404_NOT_FOUND),
        ("invalid_id", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_get_student_by_id(
    student_id: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the getting a student by ID.
    :param student_id: Student ID.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.get(
        BASE_API_URL + f"/students/{student_id}",
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert "id" in response_data
        assert "class_name" in response_data
        assert "first_name" in response_data
        assert "last_name" in response_data
        assert "age" in response_data
        assert "scores" in response_data


@pytest.mark.parametrize(
    "page, size, status_code",
    PAGINATION_VALIDATION_DATA,
)
async def test_get_all_students_with_pagination(
    page: int | Any,
    size: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the getting all students with pagination.
    :param page: Current page.
    :param size: Quantity of items per page.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.get(
        BASE_API_URL + "/students/all",
        params={
            "page": page,
            "size": size,
        },
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert "items" in response_data
        assert "total" in response_data
        assert "page" in response_data
        assert "size" in response_data
        assert "pages" in response_data


@pytest.mark.parametrize(
    "student_id, class_name, first_name, last_name, age, status_code",
    [
        (
            100_000,
            STUDENT.class_name.value,
            STUDENT.first_name,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            2,
            "invalid_class_name",
            STUDENT.first_name,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            2,
            STUDENT.class_name.value,
            "too_long_first_name" * 8,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            2,
            STUDENT.class_name.value,
            STUDENT.first_name,
            "too_long_last_name" * 8,
            STUDENT.age,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            2,
            STUDENT.class_name.value,
            STUDENT.first_name,
            STUDENT.last_name,
            1,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            2,
            None,
            None,
            None,
            None,
            status.HTTP_200_OK,
        ),
        (
            2,
            STUDENT.class_name.value,
            STUDENT.first_name,
            STUDENT.last_name,
            STUDENT.age,
            status.HTTP_200_OK,
        ),
    ],
)
async def test_update_student(
    student_id: int,
    class_name: str | Any,
    first_name: str | Any,
    last_name: str | Any,
    age: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the updating a student by ID.
    :param student_id: Student ID.
    :param class_name: New student's class type.
    :param first_name: New student's first name
    :param last_name: New student's last name.
    :param age: New student's age.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.patch(
        BASE_API_URL + f"/students/{student_id}",
        json={
            "class_name": class_name,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
        },
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert len(response_data) == 1
        assert "student_id" in response_data


@pytest.mark.parametrize(
    "student_id, status_code",
    DELETE_VALIDATION_DATA,
)
async def test_delete_student(
    ac: AsyncClient,
    student_id: int | Any,
    status_code: int,
):
    """
    Testing the deleting a student by ID.
    :param student_id: Student ID.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.delete(
        BASE_API_URL + f"/students/{student_id}",
    )
    assert response.status_code == status_code
