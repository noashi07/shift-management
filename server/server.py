import socket
import threading
import json

from db import get_session
from models.user import User

db = get_session()


def handle_routing(request):
    request_line = request.splitlines()[0]

    try:
        method, path, _ = request_line.split()

        if method == "GET" and path == "/user":
            new_user = User(username="Noa", password="123")
            db.add(new_user)
            db.commit()
            return new_user, 200

        return [{"error": "Not Found"}], 404
    except Exception as err:
        return [{"error": "Bad Request", "reason": str(err)}], 400


def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()

        response_body, status_code = handle_routing(request)
        response_body_json = json.dumps(response_body)

        status_message = "OK" if status_code == 200 else "Error"

        response = (f"HTTP/1.1 {status_code} {status_message}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(response_body_json)}\r\n\r\n"
                    f"{response_body_json}")

        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()


def start_server(hostname: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    print(f"Server started on http://{hostname}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            client_thread = threading.Thread(target=handle_request, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        db.close()
        server_socket.close()


if __name__ == "__main__":
    hostname = 'localhost'
    port = 8080

    start_server(hostname, port)
