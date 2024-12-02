import socket
import json
import threading
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional


# -------------------- Connection Parameter Classes --------------------


class ServerConnectionParameters:
    """
    Encapsulates connection parameters specific to the TCP server.

    Attributes:
        address (str): IP address to bind the server to.
        port (int): Port number to bind the server to.
        maximum_clients (int): Maximum number of concurrent clients.
        is_relay (bool): Specify if it's a message relay server
    """

    def __init__(
        self, address: str, port: int, maximum_clients: int = 5, is_relay: bool = False
    ):
        self.address = address
        self.port = port
        self.maximum_clients = maximum_clients
        self.is_relay = is_relay


class ClientConnectionParameters:
    """
    Encapsulates connection parameters specific to the TCP client.

    Attributes:
        address (str): Server's IP address to connect to.
        port (int): Server's port to connect to.
    """

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        


# ------------------------ Data Processor Classes ------------------------


class DataProcessor(ABC):
    """
    Abstract base class for processing data to and from the web.
    """

    @abstractmethod
    def from_web(self, data: bytes) -> Any:
        """
        Converts web data (bytes) to a Python object.
        """
        pass

    @abstractmethod
    def to_web(self, data: Any) -> bytes:
        """
        Converts a Python object to web data (bytes).
        """
        pass


class JsonDataProcessor(DataProcessor):
    """
    Concrete implementation of DataProcessor for JSON serialization/deserialization.
    """

    def from_web(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))

    def to_web(self, data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")


# ----------------------------- TCPClient -----------------------------


class TCPClient:
    """
    A TCP client for establishing a connection with a server and exchanging JSON-based messages. 
    This class handles sending and receiving serialized data, as well as managing connection states.
    """

    def __init__(self, params: ClientConnectionParameters):
        """
        Initializes the TCP client.

        Args:
            params (ClientConnectionParameters): Configuration parameters for the client, including
                                                  server address, port, and other connection details.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.connected_at: Optional[Tuple[str, int]] = None
        self.params = params

    def connect(self, timeout: float) -> None:
        """
        Establishes a connection to the server using the provided connection parameters.

        This method attempts to connect to the server specified by the address and port in the 
        `params` attribute. A timeout can be specified to limit how long the connection attempt 
        lasts.

        Args:
            timeout (float): The timeout in seconds for the connection attempt.

        Raises:
            Exception: If the connection cannot be established within the given timeout.
        """
        print(f"Connecting to {self.params.address}:{self.params.port}")

        try:
            if timeout:
                self.client_socket.settimeout(timeout)
            self.client_socket.connect((self.params.address, self.params.port))
            self.is_connected = True
            self.connected_at = (self.params.address, self.params.port)
            print("Successfully connected!")
            return(f"Client successfully connected at address: {self.connected_at[0]}, port: {self.connected_at[1]}")
        except Exception as e:
            print(f"Connection error: {e}")

    def send_as_json(self, data: Any, timeout: float) -> Any:
        """
        Sends data as a JSON-encoded message to the server and retrieves the response.

        This method serializes the input data to JSON, sends it to the connected server, and
        then waits for a response. The response is also expected to be in JSON format and is
        deserialized before being returned.

        Args:
            data (Any): Data to send, which will be serialized into JSON.
            timeout (float): Timeout in seconds for both the send and receive operations.

        Returns:
            Any: The JSON-decoded response from the server.

        Raises:
            Exception: If the client is not connected to a server or if the sending or receiving
                        operation encounters an error.
        """
        if not self.is_connected:
            raise Exception("Not connected to a server.")

        try:
            processor = JsonDataProcessor()
            if timeout:
                self.client_socket.settimeout(timeout)
            self.client_socket.sendall(processor.to_web(data))  # Send serialized data
            response = self.client_socket.recv(1024)  # Receive server's response
            return processor.from_web(response)  # Deserialize and return the response
        except socket.timeout:
            print(f"Request timed out after {timeout} seconds.")
        except Exception as e:
            print(f"Error sending data: {e}")
            self._close_connection()

    def ping(self, timeout: float) -> bool:
        """
        Sends a ping message to check if the client is still connected to the server.

        Args:
            timeout (float): Timeout in seconds for the ping request.

        Returns:
            bool: True if the server responds to the ping, False if not.

        Raises:
            Exception: If the client is not connected to the server or if there is a communication error.
        """
        if not self.is_connected:
            raise Exception("Not connected to a server.")

        try:
            # Sending a simple "ping" message to the server
            ping_message = {"ping": "test"}
            response = self.send_as_json(ping_message, timeout)

            # Check if the response is valid and corresponds to a "pong" message
            if response and response.get("pong") == "test":
                print("Ping successful, connection is active.")
                return True
            else:
                print("Ping failed, invalid response.")
                return False
        except Exception as e:
            print(f"Error during ping: {e}")
            return False

    def _close_connection(self) -> None:
        """
        Closes the socket connection safely.

        This internal method ensures that the connection is properly closed by terminating
        the socket and setting the connection state to `False`.
        """
        if self.is_connected:
            self.client_socket.close()
            self.is_connected = False
            print("Connection closed.")

    def close(self) -> None:
        """
        Explicitly close the TCP connection.

        This method provides an interface to explicitly close the connection from the outside.
        It invokes the `_close_connection` method to perform the actual disconnection.
        """
        self._close_connection()


    


    


# ----------------------------- TCPServer -----------------------------


class TCPServer:
    """
    A multithreaded TCP server for handling client connections and JSON-based communication.
    """

    def __init__(self, params: ServerConnectionParameters):
        """
        Initializes the TCP server.

        Args:
            params (ServerConnectionParameters): Configuration parameters for the server.
        """
        self.params = params
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.lock = threading.Lock()

    def _bind(self) -> None:
        self._server_socket.bind((self.params.address, self.params.port))

    def _listen(self) -> None:
        self._server_socket.listen(self.params.maximum_clients)
        print(f"Server listening on {self.params.address}:{self.params.port}")

    def _accept_connections(self) -> None:
        try:
            while True:
                client_socket, client_address = self._server_socket.accept()
                print(f"New connection from {client_address}")
                with self.lock:
                    self.clients[client_address] = client_socket
                threading.Thread(
                    target=self.handle, args=(client_socket, client_address)
                ).start()
        except Exception as e:
            print(f"Error accepting connections: {e}")
        finally:
            self._server_socket.close()

    def start_server(self, as_daemon: bool = False) -> None:
        """
        Starts the server.
        """
        try:
            self._bind()
            self._listen()
            print("Server is ready for connections.")
            if as_daemon:
                threading.Thread(target=self._accept_connections, daemon=True).start()
            else:
                self._accept_connections()
        except Exception as e:
            print(f"Error starting server: {e}")

    def handle(
        self, client_socket: socket.socket, client_address: Tuple[str, int]
    ) -> None:
        """
        Handles communication with a single client.
        """
        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                processor = JsonDataProcessor()
                data = processor.from_web(message)
                print(f"SERVER SAYS: Message from {client_address}: {data}")
                client_socket.sendall(processor.to_web(data))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            with self.lock:
                del self.clients[client_address]
            client_socket.close()
            print(f"Client {client_address} disconnected")


# -------------------------- TCPRelayServer --------------------------


class TCPRelayServer(TCPServer):
    """
    A TCP relay server that broadcasts messages received from one client to all other connected clients.
    """

    def handle(
        self, client_socket: socket.socket, client_address: Tuple[str, int]
    ) -> None:
        """
        Handles communication with a single client and relays their messages to all other clients.
        """
        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                processor = JsonDataProcessor()
                data = processor.from_web(message)
                print(f"SERVER SAYS: Message from {client_address}: {data}")
                # Relay the message to other clients
                with self.lock:
                    for address, socket in self.clients.items():
                        if address != client_address:
                            socket.sendall(processor.to_web(data))
                client_socket.sendall(processor.to_web({"Status": "OK"}))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            with self.lock:
                del self.clients[client_address]
            client_socket.close()
            print(f"Client {client_address} disconnected")


from typing import Union


async def setup_server(
    params: ServerConnectionParameters, 
    as_daemon: bool = True
) -> Union[TCPServer, TCPRelayServer]:
    """
    Sets up and starts a TCP server based on the provided parameters.

    This function initializes either a standard TCP server or a relay server
    depending on the `is_relay` attribute of the `ServerConnectionParameters`.
    The server starts immediately and can run in the foreground or as a daemon thread.

    Args:
        params (ServerConnectionParameters):
            The connection parameters for the server, including:
                - address (str): The IP address to bind the server to.
                - port (int): The port to bind the server to.
                - maximum_clients (int): The maximum number of concurrent clients.
                - is_relay (bool): If True, creates a relay server; otherwise, creates a standard server.

        as_daemon (bool, optional):
            Whether to run the server as a background daemon thread.
            Defaults to True.

    Returns:
        Union[TCPServer, TCPRelayServer]:
            The initialized and started server instance. Returns:
                - TCPServer: If `is_relay` is False.
                - TCPRelayServer: If `is_relay` is True.

    Raises:
        Exception:
            If the server fails to start due to binding or threading errors.

    Example:
        >>> params = ServerConnectionParameters(
        ...     address='127.0.0.1', port=8080, maximum_clients=5, is_relay=False
        ... )
        >>> server = setup_server(params)
        >>> # The server is now running in the background (as a daemon).
    """
    if params.is_relay:
        server = TCPRelayServer(params)
        print("Setting up a relay server...")
    else:
        print("Setting up a standard server...")
        server = TCPServer(params)

    server.start_server(as_daemon=as_daemon)
    return server

def setup_client(
    params: ClientConnectionParameters
) -> TCPClient:
    """
    Sets up and connects a TCP client to a server.

    This function initializes a TCP client, connects it to a server
    using the provided connection parameters, and returns the connected client.

    Args:
        params (ClientConnectionParameters):
            The connection parameters for the client, including:
                - address (str): The server's IP address to connect to.
                - port (int): The server's port to connect to.
                - timeout (float): The connection timeout in seconds.

    Returns:
        TCPClient:
            The connected TCPClient instance.

    Raises:
        Exception:
            If the connection to the server fails.

    Example:
        >>> params = ClientConnectionParameters(
        ...     address='127.0.0.1', port=8080, timeout=5.0
        ... )
        >>> client = setup_client(params)
        >>> # The client is now connected to the server and ready to send/receive data.
    """
    print(f"Setting up a client to connect to {params.address}:{params.port}...")
    
    # Initialize the client
    client = TCPClient(params)
    
    # Connect to the server
    try:
        client.connect(timeout=5)
        print(f"Client connected to {params.address}:{params.port}")
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        raise
    
    return client



