from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, TypeAlias
from client.mongo import DBClient
import os
from dotenv import load_dotenv
from validators import validators

# Load environment variables
load_dotenv()

# Type alias for validator type
ValidatorDType: TypeAlias = Any

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'db': 'movie_db',
    'username': os.getenv('ROOT_USERNAME'),
    'password': os.getenv('ROOT_PASSWORD')
}

# Initialize database client
client = DBClient(**DB_CONFIG)
db = client.db

# FastAPI app instance
app = FastAPI(
    title="Movie Database API",
    description="A simple API to interact with the movie database.",
    version="1.0.0"
)


@app.get("/", summary="Root Endpoint", tags=["Utility"])
async def root():
    """
    Root endpoint providing a welcome message.
    """
    return {"Message": "Use me to talk to the database"}


@app.get("/ping/", summary="Ping Database", tags=["Utility"])
async def ping():
    """
    Checks the connection status with the database.
    """
    return client.ping()


def initialize_collections(validators: Dict[str, ValidatorDType]):
    """
    Initializes database collections with specified validators.
    """
    for name, validator in validators.items():
        create_collection_with_validator(name, validator)
    print("Collections initialized successfully.")


def create_collection_with_validator(name: str, validator: ValidatorDType):
    """
    Creates a database collection with a given validator if it does not already exist.
    
    Parameters:
    - name: str
        Name of the collection to create.
    - validator: ValidatorDType
        Validation schema for the collection.
    """
    try:
        # Check if collection already exists
        if name in db.list_collection_names():
            print(f"Collection '{name}' already exists. Skipping creation.")
            return

        # Create collection with validator if it doesn't exist
        db.create_collection(name, validator=validator)
        print(f"Collection '{name}' created with validator.")
    except Exception as e:
        print(f"Error creating collection '{name}': {e}")
        raise HTTPException(status_code=500, detail=f"Could not create collection '{name}': {str(e)}")



# Initialize collections on startup
if __name__ == "__main__":
    print("Starting Movie Database API...")
    initialize_collections(validators)

    import uvicorn
    uvicorn.run("data_app:app", reload=True)
