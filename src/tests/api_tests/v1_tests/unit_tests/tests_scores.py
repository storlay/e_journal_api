from datetime import date
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient

from src.tests.api_tests.v1_tests.conftest import BASE_API_URL
from src.tests.api_tests.v1_tests.unit_tests.conftest import (
    DELETE_VALIDATION_DATA,
    PAGINATION_VALIDATION_DATA,
    SCORE,
)


@pytest.mark.parametrize(
    "date_of_receipt, score, student_id, status_code",
    [
        (
            date(year=9999, month=12, day=31).isoformat(),
            SCORE.score,
            7,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            SCORE.date_of_receipt.isoformat(),
            100,
            7,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            SCORE.date_of_receipt.isoformat(),
            SCORE.score,
            100_000_000,
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            SCORE.date_of_receipt.isoformat(),
            SCORE.score,
            7,
            status.HTTP_201_CREATED,
        ),
    ],
)
async def test_add_score(
    date_of_receipt: date | Any,
    score: int | Any,
    student_id: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the adding of a score.
    :param date_of_receipt: Date of receipt of the score.
    :param score: Score.
    :param student_id: ID of the student who received the score.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.post(
        BASE_API_URL + "/scores/add",
        json={
            "date_of_receipt": date_of_receipt,
            "score": score,
            "student_id": student_id,
        },
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert len(response_data) == 1
        assert "score_id" in response_data


@pytest.mark.parametrize(
    "score_id, status_code",
    [
        (2, status.HTTP_200_OK),
        (4, status.HTTP_200_OK),
        (100_000, status.HTTP_404_NOT_FOUND),
        ("invalid_id", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_get_score_by_id(
    score_id: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the getting of a score by ID.
    :param score_id: Score ID.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.get(
        BASE_API_URL + f"/scores/{score_id}",
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert "id" in response_data
        assert "date_of_receipt" in response_data
        assert "score" in response_data
        assert "student_id" in response_data


@pytest.mark.parametrize(
    "page, size, status_code",
    PAGINATION_VALIDATION_DATA,
)
async def test_get_all_scores_with_pagination(
    page: int | Any,
    size: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the getting all scores with pagination.
    :param page: Current page.
    :param size: Quantity of items per page.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.get(
        BASE_API_URL + "/scores/all",
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
    "score, status_code",
    [
        (2, status.HTTP_200_OK),
        (4, status.HTTP_200_OK),
        ("invalid_score", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_update_score(
    score: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the updating a score by ID.
    :param score: New score.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.patch(
        BASE_API_URL + f"/scores/1",
        json={
            "score": score,
        },
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_data = response.json()
        assert len(response_data) == 1
        assert "score_id" in response_data


@pytest.mark.parametrize(
    "score_id, status_code",
    DELETE_VALIDATION_DATA,
)
async def test_delete_student(
    score_id: int | Any,
    status_code: int,
    ac: AsyncClient,
):
    """
    Testing the deleting a score by ID.
    :param score_id: Score ID.
    :param status_code: API response code.
    :param ac: Async client for testing endpoints.
    """
    response = await ac.delete(
        BASE_API_URL + f"/scores/{score_id}",
    )
    assert response.status_code == status_code
