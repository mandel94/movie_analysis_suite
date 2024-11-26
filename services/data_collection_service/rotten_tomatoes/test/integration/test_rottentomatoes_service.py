import pytest
from rotten_tomatoes.rotten_tomatoes_service import RottenTomatoesService


pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="module")
def service():
    return RottenTomatoesService()

@pytest.mark.asyncio
async def test_get_movie_request(service):
    try:
        movie = await service.get_movie(movie_name="Avatar")
        print(movie)
    except Exception as e:
        assert False, f"An error occured: {e}"
