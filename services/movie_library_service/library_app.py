from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Movie Library API",
    description="A simple API to interact with the movie library.",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",  # Allow your frontend (e.g., Next.js or React)
    "https://your-frontend-domain.com",  # Add other domains here
    "*",  # Allow all origins (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies or credentials to be sent
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in the request
)


@app.get("/", summary="Root Endpoint", tags=["Utility"])
async def read_root():
    """
    A root endpoint to provide a welcome message for users.

    **Returns**:
    - A JSON message confirming the API's purpose.

    Example response:
    ```
    {
        "Message": "Welcome to the Movie Library API"
    }
    ```
    """
    return {"Message": "Welcome to the Movie Library API"}


@app.get("/movie/", summary="Get All Movies", tags=["Movies"])
async def get_all_movies():
    """
    Retrieve all movies from the database.

    **Returns**:
    - A JSON response with all the movies in the database.

    Example response:
    ```
    [
        {
            "Title": "The Shawshank Redemption",
            "Year": 1994,
            "Genre": "Drama"
        },
        {
            "Title": "The Godfather",
            "Year": 1972,
            "Genre": "Crime"
        }
    ]
    ```
    """
    return [
        {"Title": "The Shawshank Redemption", "Year": 1994, "Genre": "Drama"},
        {"Title": "The Godfather", "Year": 1972, "Genre": "Crime"},
        {"Title": "The Dark Knight", "Year": 2008, "Genre": "Action"},
    ]


@app.get("/movie/{title}", summary="Get Movie by Title", tags=["Movies"])
async def get_movie_by_title(title: str):
    """
    Retrieve a movie from the database by its title.

    **Parameters**:
    - title: The title of the movie to retrieve.

    **Returns**:
    - A JSON response with the movie details.

    Example response:
    ```
    {
        "Title": "The Shawshank Redemption",
        "Year": 1994,
        "Genre": "Drama"
    }
    ```
    """
    return {"Message": f"Get movie by title: {title}"}





if __name__ == "__main__":
    import uvicorn

    uvicorn.run("library_app:app", host="localhost", port=8000, reload=True)
