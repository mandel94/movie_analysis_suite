import pytest
from rotten_tomatoes.connections import TCPClient, TCPServer, TCPRelayServer
import threading
import time

@pytest.fixture(scope="module")
def address():
    """Fixture for the server address."""
    return "127.0.0.1"

@pytest.fixture(scope="module")
def port():
    """Port exposed by the server."""
    return 65432

@pytest.fixture(scope="module")
def relay_server(address, port):
    """Fixture for the TCPRelayServer."""
    relay_server = TCPRelayServer(address, port)
    thread = threading.Thread(target=relay_server.start_server, args=(True,))
    thread.start()
    # Wait briefly to ensure the server starts
    time.sleep(1)
    return relay_server

@pytest.fixture
def client_factory(address, port):
    """Fixture to create multiple clients."""
    def create_client():
        client = TCPClient()
        client.connect(address=address, port=port)
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
        client1.send_as_json(data=message)

        # Verify that client2 receives the message
        response = client2.client_socket.recv(1024).decode("utf-8")
        assert "Hello from client1" in response, "Client2 did not receive the relayed message from Client1"
    finally:
        # Clean up clients
        client1.close()
        client2.close()
