from fastapi import APIRouter, HTTPException, BackgroundTasks
from rotten_tomatoes_service import RottenTomatoesService
from models import Review, Movie, Author
from typing import List, Optional

router = APIRouter()
service = RottenTomatoesService()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Rotten Tomatoes API"}

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
