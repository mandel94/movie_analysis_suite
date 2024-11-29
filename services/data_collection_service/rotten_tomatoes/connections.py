import socket
import json
import threading
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional


class TCPClient:
    """
    A TCP client for connecting to a server and exchanging JSON-based messages.

    Attributes:
        client_socket (socket.socket): The client's socket object.
        is_connected (bool): Connection status.
        connected_at (Optional[Tuple[str, int]]): Server address and port, if connected.
        timeout (float): Timeout for socket operations in seconds (default: 5.0).
    """

    def __init__(self):
        """
        Initializes the TCP client.
        """
        self.client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected: bool = False
        self.connected_at: Optional[Tuple[str, int]] = None
        self.timeout: float = 5.0  # Timeout for socket operations in seconds

    def connect(self, address: str, port: int) -> None:
        """
        Establish a connection to the server.

        Args:
            address (str): Server's IP address.
            port (int): Server's port.

        Raises:
            Exception: If unable to connect to the server.
        """
        self.address = address
        self.port = port
        print(f"Connecting to {address}:{port}")

        try:
            self.client_socket.connect((self.address, self.port))
            self.client_socket.settimeout(self.timeout)
            self.is_connected = True
            self.connected_at = (address, port)
            print("Successfully connected!")
        except Exception as e:
            print(f"Connection error: {e}")

    def send_as_json(self, data: Any) -> Any:
        """
        Sends data as JSON to the server and retrieves the response.

        Args:
            data (Any): Data to send (serializable to JSON).

        Returns:
            Any: Response received from the server.

        Raises:
            Exception: If not connected to the server or an error occurs during data transmission.
        """
        if not self.is_connected:
            raise Exception("Not connected to a server.")

        try:
            json_data = JsonDataProcessor().to_web(data)
            self.client_socket.sendall(json_data)
            response = self.client_socket.recv(1024)
            if response:
                print("Server response:", JsonDataProcessor().from_web(response))
                return JsonDataProcessor().from_web(response)
        except socket.timeout:
            print(f"Request timed out after {self.timeout} seconds.")
        except Exception as e:
            print(f"Error sending data: {e}")
            self._close_connection()

    def _close_connection(self) -> None:
        """
        Closes the socket connection safely.
        """
        if self.is_connected:
            self.client_socket.close()
            print(f"Connection closed.")
            self.is_connected = False

    def close(self) -> None:
        """
        Explicitly close the connection.
        """
        self._close_connection()


class DataProcessor(ABC):
    """
    Abstract base class for processing data to and from the web.
    """

    @abstractmethod
    def from_web(self, data: bytes) -> Any:
        """
        Converts web data (bytes) to a Python object.

        Args:
            data (bytes): Data received from the web.

        Returns:
            Any: Deserialized Python object.
        """
        pass

    @abstractmethod
    def to_web(self, data: Any) -> bytes:
        """
        Converts a Python object to web data (bytes).

        Args:
            data (Any): Python object to serialize.

        Returns:
            bytes: Serialized byte data.
        """
        pass


class JsonDataProcessor(DataProcessor):
    """
    Concrete implementation of DataProcessor for JSON serialization/deserialization.
    """

    def from_web(self, data: bytes) -> Any:
        """
        Deserializes JSON data from bytes.

        Args:
            data (bytes): JSON data as bytes.

        Returns:
            Any: Deserialized Python object.
        """
        return json.loads(data.decode("utf-8"))

    def to_web(self, data: Any) -> bytes:
        """
        Serializes Python data to JSON bytes.

        Args:
            data (Any): Python object to serialize.

        Returns:
            bytes: JSON data as bytes.
        """
        return json.dumps(data).encode("utf-8")


class TCPServer:
    """
    A multithreaded TCP server for handling client connections and JSON-based communication.

    Attributes:
        address (str): Server's IP address.
        port (int): Server's port.
        maximum_clients (int): Maximum number of concurrent clients.
        clients (dict): Dictionary of connected clients (address: socket).
        lock (threading.Lock): Thread lock for synchronizing client access.
    """

    def __init__(self, address: str, port: int, maximum_clients: int = 5) -> None:
        """
        Initializes the TCP server.

        Args:
            address (str): Server's IP address.
            port (int): Server's port.
            maximum_clients (int, optional): Maximum concurrent clients (default: 5).
        """
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.address = address
        self.port = port
        self.maximum_clients = maximum_clients
        self.clients = {}
        self.lock = threading.Lock()

    def _bind(self) -> None:
        """
        Binds the server socket to the specified address and port.
        """
        self._server_socket.bind((self.address, self.port))

    def _listen(self) -> None:
        """
        Starts listening for incoming connections.
        """
        self._server_socket.listen(self.maximum_clients)
        print(f"Server listening on {self.address}:{self.port}")

    def _accept_connections(self) -> None:
        """
        Accepts client connections and spawns threads to handle each client.
        """
        try:
            while True:
                client_socket, client_address = self._server_socket.accept()
                print(f"New connection from {client_address}")
                with self.lock:
                    self.clients[client_address] = client_socket
                thread = threading.Thread(
                    target=self.handle, args=(client_socket, client_address)
                )
                thread.start()
        except Exception as e:
            print(f"Error accepting connections: {e}")
        finally:
            self._server_socket.close()

    def start_server(self, as_daemon: bool = False) -> None:
        """
        Starts the server.

        Args:
            as_daemon (bool, optional): Whether to run the server in the background (default: False).
        """
        try:
            self._bind()
            self._listen()
            print("Server is ready for connections.")
            if as_daemon:
                thread = threading.Thread(target=self._accept_connections, daemon=True)
                thread.start()
            else:
                self._accept_connections()
        except Exception as e:
            print(f"Error starting server: {e}")

    def handle(self, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        """
        Handles communication with a single client.

        Args:
            client_socket (socket.socket): Client's socket.
            client_address (Tuple[str, int]): Client's address.
        """
        try:
            while True:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                print(f"Message from {client_address}: {message}")
                client_socket.sendall(JsonDataProcessor().to_web(message))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            with self.lock:
                del self.clients[client_address]
            client_socket.close()
            print(f"Client {client_address} disconnected")


class TCPRelayServer(TCPServer):
    """
    A TCP relay server that broadcasts messages received from one client to all other connected clients.
    """

    def handle(self, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        """
        Handles communication with a single client and relays their messages to all other clients.

        Args:
            client_socket (socket.socket): Client's socket.
            client_address (Tuple[str, int]): Client's address.
        """
        try:
            while True:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                print(f"Message from {client_address}: {message}")
                client_socket.sendall(JsonDataProcessor().to_web(message))
                # Relay the message to other clients
                with self.lock:
                    for address, socket in self.clients.items():
                        if address != client_address:
                            socket.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            with self.lock:
                del self.clients[client_address]
            client_socket.close()
            print(f"Client {client_address} disconnected")
