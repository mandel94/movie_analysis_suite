import socket
import json
import threading


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
            json_data = json.dumps(data).encode("utf-8")
            self.client_socket.send(json_data)
        except Exception:
            raise

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

    def send_data_as_json(self, data):
        try:
            self._ensure_connected()
            self._send_as_json(data)
            response = self.client_socket.recv(1024)
            print("Server response:", response.decode("utf-8"))
            self._close_connection()
            return response
        except Exception as e:
            raise Exception("Error when sending data: {e}")


def _json_receive(data):
    return json.loads(data.decode("utf-8"))


def _return_success_as_json(data):
    json_response = json.dumps({"status": "success", "data": data}).encode("utf-8")
    return json_response


def default_handler(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            received_data = _json_receive(data)
            print("Received data:", received_data)
            response = _return_success_as_json(received_data)
            client_socket.send(response)
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()


class TCPServer:
    def __init__(self, address, port, handle_client=None, maximum_clients=5):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if handle_client is None:
            self.handle_client = default_handler
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
            self.handle_client(client_socket)

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
