import socket
import threading
import json

from sqlalchemy import update

from models.user import User
from models.db.db import get_session, init_db

session = get_session()
init_db()


def extract_body_from_request(request: str):
    # Split the request by the double newline to separate headers from body
    headers, body = request.split("\r\n\r\n", 1)

    # Check if body is in JSON format, which is common for POST requests
    try:
        # Parse the body using json.loads() and return the resulting dictionary
        body_dict = json.loads(body)
        return body_dict
    except json.JSONDecodeError:
        # Handle error in case the body is not valid JSON
        print("Error: Body is not valid JSON")
        return None


def handle_routing(request):
    request_line = request.splitlines()[0]

    try:
        method, path, _ = request_line.split()

        route_parameters = str(path).split('/')[2:]

        if method == "PATCH" and 'user' in path:
            data = extract_body_from_request(request)
            user_id = route_parameters[0]

            user = session.query(User).filter(User.id == user_id).first()

            if data["username"] is not None:
                user.username = data["username"]
            if data["password"] is not None:
                user.password = data["password"]

            session.commit()

            return json.loads(user.__repr__()), 200

        if method == "GET" and path == "/users":
            users = [json.loads(user.__repr__()) for user in session.query(User).all()]

            return users, 200

        if method == "POST" and path == "/user":
            data = extract_body_from_request(request)

            # יצירת משתמש חדש עם שם משתמש וסיסמא מתוך הבקשה
            new_user = User(username=data['username'], password=data['password'])
            session.add(new_user)
            session.commit()
            return new_user.__repr__(), 200

        return [{"error": "Not Found"}], 404
    except Exception as err:
        session.rollback()
        return [{"error": "Bad Request", "reason": str(err)}], 400


def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()

        # אם התהליך הצליח נקבל קוד 200 ואובייקט מסוג USER שנוצר מהמידע ששלח הלקוח
        response_body, status_code = handle_routing(request)
        # ממיר את האובביט מסוג User ל-json
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
        session.close()
        server_socket.close()


if __name__ == "__main__":
    hostname = 'localhost'
    port = 8080

    start_server(hostname, port)
