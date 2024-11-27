import socket
import json
import threading
from abc import ABC, abstractmethod
from typing import Literal, Any, Tuple, Optional


class TCPClient:
    def __init__(self):
        self.client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected: bool = False
        self.connected_at: Optional[Tuple[str, int]] = None

    def _ensure_connected(self) -> None:
        try:
            if not self.is_connected:
                self.client_socket.connect((self.address, self.port))
        except Exception as e:
            raise Exception(f"Error when calling self._ensure_connected: {e}")

    def _send_as_json(self, data: Any) -> bytes:
        try:
            json_data = JsonDataProcessor().to_web(data)
            self.client_socket.send(json_data)
            response = self.client_socket.recv(1024)
            return response
        except Exception as e:
            raise Exception(f"Error when sending data as json: {e}")

    def _close_connection(self) -> None:
        if self.connected_at:
            address, port = self.connected_at
            self.client_socket.close()
            print(f"Client: Connection closed at host {address} / port {port}")
            self.is_connected = False

    def connect(self, address: str, port: int) -> None:
        print(f"Connecting to {address}:{port}")
        self.client_socket.connect((address, port))
        self.is_connected = True
        self.connected_at = (address, port)
        print(f"Successfully connected!")

    def send_as_json(self, data: Any) -> Any:
        try:
            self._ensure_connected()
            response = self._send_as_json(data)
            print("Server response:", response.decode("utf-8"))
            return response
        except Exception as e:
            raise Exception(f"Error when sending data: {e}")
        finally:
            self._close_connection()


class DataProcessor(ABC):
    @abstractmethod
    def from_web(self, data: bytes) -> Any:
        pass

    @abstractmethod
    def to_web(self, data: Any) -> bytes:
        pass


class JsonDataProcessor(DataProcessor):
    def from_web(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))

    def to_web(self, data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")


class Response(ABC):
    @abstractmethod
    def from_data(self, status: str, data: Any) -> bytes:
        pass


class JsonResponse(Response):
    def from_data(self, status: str, data: Any) -> bytes:
        response = json.dumps({"status": status, "data": data}).encode("utf-8")
        return response



class TCPServer:
    def __init__(self, address: str, port: int, maximum_clients: int = 5) -> None:
        self._server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.maximum_clients: int = maximum_clients
        self.address: str = address
        self.port: int = port
        self.clients = {}

    def _bind(self, address: str, port: int) -> None:
        try:
            self.address = address
            self.port = port
            self._server_socket.bind((address, port))
        except Exception as e:
            raise Exception(
                f"Error when binding the server to address {address} at port {port}:\n{e}"
            )

    def _listen(self, backlog: int) -> None:
        self._server_socket.listen(backlog)
        print(f"Server listening on {self.address}:{self.port}")

    def _accept_connections(self) -> None:
        try:
            while True:
                client_socket, client_address = self._server_socket.accept()
                print(f"New connection from {client_address}")
                self.clients[client_address] = client_socket
                thread = threading.Thread(target=TCPServer.handle_client, args=(client_socket, client_address))
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down the server...")


    def start_server(self, as_daemon: bool = False) -> str:
        try:
            print("Starting server...")
            self._bind(self.address, self.port)
            print("Server bound to address")
            self._listen(self.maximum_clients)
            print("Server listening for connections")
            if as_daemon:
                thread = threading.Thread(target=self._accept_connections, daemon=True)
                thread.start()
            else:
                self._accept_connections()
            return f"Server is ready to listen from host {self.address} at port {self.port}..."
        except Exception as e:
            raise Exception(f"Error from the server: {e}")
    
    
    def handle_client(self, client_socket, client_address):
        try:
            while True:
                # Receive message from the client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break  # Connection closed by client

                print(f"Message from {client_address}: {message}")

                # Relay the message to all other connected clients
                for addr, sock in self.clients.items():
                    if addr != client_address:  # Don't send the message back to the sender
                        sock.send(f"Message from {client_address}: {message}".encode('utf-8'))
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
        finally:
            # Remove the client and close the connection
            print(f"Client {client_address} disconnected")
            del self.clients[client_address]
            client_socket.close()
        
