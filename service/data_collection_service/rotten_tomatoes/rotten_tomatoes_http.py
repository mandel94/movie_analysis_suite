from fastapi import FastAPI
from api.endpoints import router as api_router

<<<<<<< HEAD

=======
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
app = FastAPI(title="Rotten Tomatoes API", description="API for movie details and reviews")

# Include API endpoints
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rotten_tomatoes_http:app", host="localhost", port=8003, reload=True)
