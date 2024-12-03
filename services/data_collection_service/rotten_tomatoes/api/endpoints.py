from fastapi import APIRouter, HTTPException, BackgroundTasks
from rotten_tomatoes_service import RottenTomatoesService
from models import Review, Movie, Author
from typing import List, Optional
from connections import (
    TCPClient,
    ClientConnectionParameters,
    ServerConnectionParameters,
    setup_server,
    setup_client,
)
import asyncio


address: str = "127.0.0.1"
port: str = 8740

router = APIRouter()


async def setup():
    server = await setup_server(
        ServerConnectionParameters(
            address=address, port=port, maximum_clients=2, is_relay=True
        )
    )

async def await_for_crawling_results():
    pass

server = asyncio.run(setup())

client_conn_params = ClientConnectionParameters(address=address, port=port)
proxy_client = setup_client(client_conn_params)

service = RottenTomatoesService()


@router.get("/")
def read_root():
    return {"message": "Welcome to the Rotten Tomatoes API"}


@router.get("/movie/{title}")  # Get movie by title
async def get_movie(title: str):

    service.get_movie(title, client_conn_params)
    movie = proxy_client.client_socket.recv(1024)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"movie": movie}


@router.get("/test/")  # Get movie by title asynchronously
def test():
    # return {"client connected": [client]}
    return proxy_client.ping(timeout=10)
