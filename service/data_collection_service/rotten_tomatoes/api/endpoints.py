<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, BackgroundTasks
=======
from fastapi import APIRouter, HTTPException
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
from rotten_tomatoes_service import RottenTomatoesService
from models import Review, Movie, Author
from typing import List, Optional

router = APIRouter()
service = RottenTomatoesService()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Rotten Tomatoes API"}

<<<<<<< HEAD
@router.get("/movie/{title}")         # Get movie by title
async def get_movie(title: str):
    movie = await service.get_movie(title)
    return movie
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"movie": movie}

@router.get("/test/")    # Get movie by title asynchronously
def test():
    test_data = service.get_test_movie()
    return {"data": test_data}
=======
@router.get("/movies/{movie_name}")
async def get_movie(movie_name: str):
    movie = await service.get_movie(movie_name)
    return movie
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/movies/{movie_name}/reviews", response_model=List[Review])
async def get_movie_reviews(movie_name: str):
    reviews = await service.get_movie_reviews(movie_name)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    return reviews

@router.get("/movies/{movie_name}/critic_reviews", response_model=List[Review])
async def get_critic_reviews(movie_name: str):
    reviews = await service.get_critics_movie_review(movie_name)
    if not reviews:
        raise HTTPException(status_code=404, detail="No critic reviews found")
    return reviews
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
