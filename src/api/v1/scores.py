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
from src.schemas.scores import (
    AddScoreSchema,
    PathScoreIdSchema,
    ScoreSchema,
    ScoreIdSchema,
    UpdateScoreSchema,
)
from src.services.scores import ScoresService


router = APIRouter(
    tags=["Scores"],
    prefix="/scores",
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Getting all scores",
    description="Getting all scores with pagination",
)
async def get_all_scores(
    transaction: TransactionDep,
    pagination: PaginationParams = Depends(),
) -> BasePaginationResponse[ScoreSchema]:
    """
    Getting all scores.
    :param transaction: Database transaction.
    :param pagination: Pagination params.
    :return: List of Pydantic models representing the scores.
    """
    return await ScoresService.get_all_scores(
        transaction,
        pagination,
    )


@router.get(
    "/{score_id}",
    status_code=status.HTTP_200_OK,
    summary="Getting a score by ID",
    description="Getting a score by ID.",
)
async def get_score(
    transaction: TransactionDep,
    score_id: PathScoreIdSchema = Depends(),
) -> ScoreSchema:
    """
    Getting a score by ID.
    :param transaction: Database transaction.
    :param score_id: Score ID.
    :return: Pydantic model representing the score.
    """
    return await ScoresService.get_score(
        transaction,
        score_id.id,
    )


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    summary="Adding a new score",
    description="Adding a new score.",
)
async def add_score(
    transaction: TransactionDep,
    score_data: AddScoreSchema,
) -> ScoreIdSchema:
    """
    Adding a new score.
    :param transaction: Database transaction.
    :param score_data: Pydantic model representing score data.
    :return: Pydantic model representing the created score ID.
    """
    return await ScoresService.add_score(
        transaction,
        score_data,
    )


@router.patch(
    "/{score_id}",
    status_code=status.HTTP_200_OK,
    summary="Updating a score by ID",
    description="Updating a score by ID.",
)
async def update_score(
    transaction: TransactionDep,
    new_score: UpdateScoreSchema,
    score_id: PathScoreIdSchema = Depends(),
) -> ScoreIdSchema:
    """
    Updating a score by ID.
    :param transaction: Database transaction.
    :param score_id: Score ID.
    :param new_score: Pydantic model representing new score.
    :return: Pydantic model representing the updated score ID.
    """
    return await ScoresService.update_score(
        transaction,
        score_id.id,
        new_score,
    )


@router.delete(
    "/{score_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a score by ID",
    description="Deleting a score by ID.",
)
async def delete_score(
    transaction: TransactionDep,
    score_id: PathScoreIdSchema = Depends(),
) -> None:
    """
    Deleting a score by ID.
    :param transaction: Database transaction.
    :param score_id: Score ID.
    :return: None.
    """
    await ScoresService.delete_score(
        transaction,
        score_id.id,
    )
