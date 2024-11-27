import pytest
from rotten_tomatoes.connections import TCPClient, TCPServer


@pytest.fixture(scope="module")
def address():
    """Fixture for the server address."""
    return "127.0.0.1"


@pytest.fixture(scope="module")
def port():
    """Port exposed by the server"""
    return 65432


@pytest.fixture(scope="module")
def server(address, port):
    server = TCPServer(address=address, port=port)
    server.start_server(as_daemon=True)
    return server


@pytest.fixture(scope="module")
def client(address, port):
    client = TCPClient()
    client.connect(address=address, port=port)
    return client


def test_tcp_connection(server, client):
    try:
        response = client.send_as_json(data={"message": "Hello, server!"})
    except Exception as e:
        assert False, f"Client did not manage to deliver message: {e}"
    assert response, "Response is void"
