from pydantic import BaseModel
from typing import Optional

class Author(BaseModel):
    name: str
    id: Optional[str]
    is_critic: bool
    stars: Optional[float]
    comment: Optional[str]
    date: Optional[str]

class Review(BaseModel):
    movie: Optional[str]  # Reference to movie title
    author: Author
    stars: Optional[float]
    comment: Optional[str]

class Movie(BaseModel):
    title: str
    year: int
    rating: str
    genre: str
    director: str
    popcornmeter: int
    tomatometer: int
    is_certified_fresh: bool
    is_verified_hot: bool
    synopsis: str
