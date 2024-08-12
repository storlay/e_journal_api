from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
)

from src.api.pagination import (
    BasePaginationResponse,
    PaginationParams,
    Paginator,
)
from src.exceptions.scores import (
    IncorrectStudentException,
    ScoreNotFoundException,
)
from src.schemas.scores import (
    AddScoreSchema,
    ScoreSchema,
    ScoreIdSchema,
    UpdateScoreSchema,
)
from src.utils.transaction import BaseManager


class ScoresService:

    @staticmethod
    async def get_all_scores(
        transaction: BaseManager,
        pagination: PaginationParams,
    ) -> BasePaginationResponse[ScoreSchema]:
        """
        The logic of getting all scores.
        :param transaction: Database transaction.
        :param pagination: Pagination params.
        :return: List of Pydantic models representing the scores.
        """
        async with transaction:
            scores = await transaction.scores_repo.find_all()
            paginator = Paginator(
                pages=scores,
                params=pagination,
            )
            return paginator.get_response()

    @staticmethod
    async def get_score(
        transaction: BaseManager,
        score_id: int,
    ) -> ScoreSchema:
        """
        The logic of getting a score by ID.
        :param transaction: Database transaction.
        :param score_id: Score ID
        :return: Pydantic model representing the score.
        """
        async with transaction:
            try:
                score = await transaction.scores_repo.find_one(
                    id=score_id,
                )
                return score
            except NoResultFound:
                raise ScoreNotFoundException

    @staticmethod
    async def add_score(
        transaction: BaseManager,
        score_data: AddScoreSchema,
    ) -> ScoreIdSchema:
        """
        The logic of creating a score.
        :param transaction: Database transaction.
        :param score_data: Pydantic model representing score data.
        :return: Pydantic model representing the created score ID.
        """
        score_data_dict = score_data.model_dump()
        async with transaction:
            try:
                score_id = await transaction.scores_repo.add_one(
                    score_data_dict,
                )
                await transaction.commit()
                return ScoreIdSchema(score_id=score_id)
            except IntegrityError:
                raise IncorrectStudentException

    @staticmethod
    async def update_score(
        transaction: BaseManager,
        score_id: int,
        new_score: UpdateScoreSchema,
    ) -> ScoreIdSchema:
        """
        The logic of updating a score by ID.
        :param transaction: Database transaction.
        :param score_id: Score ID.
        :param new_score: Pydantic model representing a new score.
        :return: Pydantic model representing the updated score ID.
        """
        new_score_dict = new_score.model_dump()
        async with transaction:
            try:
                await transaction.scores_repo.edit_one(
                    score_id,
                    new_score_dict,
                )
                await transaction.commit()
                return ScoreIdSchema(score_id=score_id)
            except NoResultFound:
                raise ScoreNotFoundException

    @staticmethod
    async def delete_score(
        transaction: BaseManager,
        score_id: int,
    ) -> None:
        """
        The logic of deleting a score by ID.
        :param transaction: Database transaction.
        :param score_id: Score ID
        :return: None.
        """
        async with transaction:
            await transaction.scores_repo.delete_one(
                score_id,
            )
            await transaction.commit()
