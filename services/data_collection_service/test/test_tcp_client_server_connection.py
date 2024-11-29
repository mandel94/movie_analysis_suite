import pytest
from rotten_tomatoes.connections import (
    TCPRelayServer,
    TCPClient,
    ServerConnectionParameters,
    setup_server,
    setup_client,
    ClientConnectionParameters,
)
import threading
import time
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="module")
def address():
    """Fixture for the server address."""
    return "127.0.0.1"


@pytest.fixture(scope="module")
def port():
    """Port exposed by the server."""
    return 65432

@pytest.fixture(scope="module")
def server_params(address, port):
    """Fixture for the server parameters."""
    return ServerConnectionParameters(
        address=address, port=port, maximum_clients=2, is_relay=True
    )

@pytest.fixture(scope="module")
def client_params(address, port):
    """Fixture for the client parameters."""
    return ClientConnectionParameters(address=address, port=port)


@pytest.fixture(scope="module")
def relay_server(server_params):
    """Fixture for the TCPRelayServer."""
    relay_server = TCPRelayServer(server_params)
    thread = threading.Thread(target=relay_server.start_server, args=(True,))
    thread.start()
    # Wait briefly to ensure the server starts
    time.sleep(1)
    return relay_server


@pytest.fixture
def client_factory(client_params):
    """Fixture to create multiple clients."""

    def create_client():
        client = TCPClient(client_params)
        client.connect(timeout=5)
        return client

    return create_client


def test_relay_message_server(relay_server, client_factory):
    """Test the message relay functionality of the TCPRelayServer."""
    # Create two clients
    client1 = client_factory()
    client2 = client_factory()

    try:
        # Send a message from client1
        message = {"message": "Hello from client1"}
        client1.send_as_json(data=message, timeout=1)

        # Verify that client2 receives the message
        response = client2.client_socket.recv(1024).decode("utf-8")
        assert (
            "Hello from client1" in response
        ), "Client2 did not receive the relayed message from Client1"
    finally:
        # Clean up clients
        client1.close()
        client2.close()


@pytest.fixture
def mock_server():
    with patch("socket.socket") as mock_socket:
        yield mock_socket


def test_setup_server(mock_server, server_params):
    setup_server(server_params)

    # Ensure socket methods are called correctly
    mock_server.return_value.bind.assert_called_with(("127.0.0.1", 65432))
    mock_server.return_value.listen.assert_called_with(2)  # Max clients



