import socket
import json
import threading
from abc import ABC, abstractmethod
from typing import Literal, Any


class TCPClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _ensure_connected(self):
        try:
            if not self.is_connected:
                self.client_socket.connect((self.address, self.port))
        except Exception as e:
            raise Exception("Error when calling self._ensure_connected: {e}")

    def _send_as_json(self, data):
        try:
            json_data = JsonDataProcessor().to_web(data)
            self.client_socket.send(json_data)
            response = self.client_socket.recv(1024)
            return response
        except Exception as e:
            raise Exception(f"Error when sending data as json: {e}")

    def _close_connection(self):
        address, port = self.connected_at
        self.client_socket.close()
        print(f"Client: Connection closed at host {address} / port {port}")
        self.is_connected = False

    def connect(self, address, port):
        print(f"Connecting to {address}:{port}")
        self.client_socket.connect((address, port))
        self.is_connected = True
        self.connected_at = (address, port)
        print(f"Successfully connected!")

    def send_as_json(self, data) -> Any:
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
    def from_web(self): ...

    @abstractmethod
    def to_web(self): ...


class JsonDataProcessor(DataProcessor):
    def from_web(self, data):
        return json.loads(data.decode("utf-8"))

    def to_web(self, data):
        return json.dumps(data).encode("utf-8")


class Response(ABC):
    @abstractmethod
    def from_data(self, data): ...


class JsonResponse(Response):
    def from_data(self, status, data) -> dict:
        response = json.dumps({"status": status, "data": data}).encode("utf-8")
        return response


class DataHandler:
    def __init__(
        self,
        client_socket: socket,
        data_processor: DataProcessor,
        response_type: Literal["json"] = "json",
    ):
        self.client_socket = client_socket
        self.data_processor = data_processor
        self.response_type = response_type

    def handle_data(self):
        try:
            data = self.client_socket.recv(1024)
            if data:
                received_data = self.data_processor.from_web(data)
                print("Received data:", received_data)
                response = DataHandler.get_response(
                    received_data, outcome="success", response_type=self.response_type
                )
                self.client_socket.send(response)
        except Exception as e:
            print("Error when handling data:", e)
        finally:
            self.client_socket.close()

    @staticmethod
    def get_response(data, outcome, response_type):
        if response_type == "json":
            return JsonResponse().from_data(status=outcome, data=data)


class TCPServer:
    def __init__(self, address, port, maximum_clients=5):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.maximum_clients = maximum_clients
        self.address = address
        self.port = port

    def _bind(self, address, port):
        try:
            self.address = address
            self.port = port
            self._server_socket.bind((address, port))
        except Exception as e:
            raise Exception(
                f"Error when binding the server to addres {address} at port {port}:\n{e}"
            )

    def _listen(self, backlog):
        self._server_socket.listen(backlog)
        print(f"Server listening on {self.address}:{self.port}")

    def _accept_connections(self):
        while True:
            client_socket, client_address = self._server_socket.accept()
            print(f"Connection established with {client_address}")
            data_handler = DataHandler(client_socket, JsonDataProcessor())
            data_handler.handle_data()

    def start_server(self, as_daemon=False):
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
            return "Server is ready to listen from host {address} at port {port}..."
        except Exception as e:
            raise Exception(f"Error from the server: {e}")
