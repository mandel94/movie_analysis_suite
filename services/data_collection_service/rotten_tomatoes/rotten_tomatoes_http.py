from fastapi import FastAPI
from api.endpoints import router as api_router
from connections import TCPClient, TCPServer

app = FastAPI(title="Rotten Tomatoes API", description="API for movie details and reviews")

# Include API endpoints
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    storage_server = TCPServer(address='127.0.0.1', port='8092')
    uvicorn.run("rotten_tomatoes_http:app", host="localhost", port=8003, reload=True)
