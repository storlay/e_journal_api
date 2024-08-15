import pytest
from httpx import AsyncClient


@pytest.fixture(scope="function")
async def ac():
    """
    Async client for testing endpoints.
    """

    async with AsyncClient(base_url="http://localhost:8080") as ac:
        yield ac
