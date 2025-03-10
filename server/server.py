import socket
import threading
import json

from models.user import User
from models.table import TableData
from models.db.db import get_session, init_db

session = get_session()
init_db()

connected_clients = []
clients_lock = threading.Lock()


def handle_http_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        if not request:
            raise ValueError("Empty request received")
        print(request)

        def extract_body_from_request(request: str):
            headers, body = request.split("\r\n\r\n", 1)
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                print("Error: Body is not valid JSON")
                return None

        def handle_routing(request):
            request_line = request.splitlines()[0]
            try:
                method, path, _ = request_line.split()
                route_parameters = str(path).split('/')[2:]

                if method == "PATCH" and 'user' in path:
                    data = extract_body_from_request(request)
                    if not data or 'username' not in data or 'password' not in data:
                        return {"error": "Bad Request", "reason": "Missing username or password"}, 400
                    user_id = route_parameters[0]
                    user = session.query(User).filter(User.id == user_id).first()
                    if user:
                        if data["username"] is not None:
                            user.username = data["username"]
                        if data["password"] is not None:
                            user.password = data["password"]
                        session.commit()
                        return json.loads(user.__repr__()), 200
                    return {"error": "Not Found", "reason": "User not found"}, 404

                if method == "DELETE" and 'user' in path:
                    user_id = route_parameters[0]
                    user = session.query(User).filter(User.id == user_id).first()
                    if user is None:
                        return {"status": "error", "message": "User not found."}, 404
                    try:
                        session.delete(user)
                        session.commit()
                        return {"status": "success", "message": f"User with ID {user_id} deleted successfully."}, 200
                    except Exception as e:
                        session.rollback()
                        return {"status": "error", "message": str(e)}, 500

                if method == "GET" and 'user' in path:
                    users = [json.loads(user.__repr__()) for user in session.query(User).all()]
                    return users, 200

                if method == "POST" and 'user/login' in path:
                    data = extract_body_from_request(request)
                    if not data or 'username' not in data or 'password' not in data:
                        return {"error": "Bad Request", "reason": "Missing username or password"}, 400
                    try:
                        user = session.query(User).filter(User.username == str(data['username']),
                                                          User.password == str(data['password'])).first()
                        if user:
                            return json.loads(user.__repr__()), 200
                        return {'error': 'Not Found',
                                'reason': f"User with username {data['username']} not found or password incorrect"}, 404
                    except Exception as e:
                        return {'error': 'Server Error', 'reason': str(e)}, 500

                if method == "POST" and 'user' in path:
                    data = extract_body_from_request(request)
                    if not data or 'username' not in data or 'password' not in data:
                        return {"error": "Bad Request", "reason": "Missing username or password"}, 400
                    new_user = User(username=data['username'], password=data['password'])
                    session.add(new_user)
                    session.commit()
                    return json.loads(new_user.__repr__()), 201

                return [{"error": "Not Found"}], 404
            except Exception as err:
                session.rollback()
                return [{"error": "Bad Request", "reason": str(err)}], 400

        response_body, status_code = handle_routing(request)
        response_body_json = json.dumps(response_body)
        status_message = "OK" if status_code in (200, 201) else "Error"
        response = (f"HTTP/1.1 {status_code} {status_message}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(response_body_json)}\r\n\r\n"
                    f"{response_body_json}")
        client_socket.sendall(response.encode())
    except Exception as e:
        error_response = json.dumps({"error": "Server Error", "message": str(e)})
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: application/json\r\nContent-Length: {len(error_response)}\r\n\r\n{error_response}"
        try:
            client_socket.sendall(response.encode())
        except:
            print(f"Failed to send error response: {e}")
    finally:
        client_socket.close()


def start_http_server(hostname: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    print(f"HTTP Server started on http://{hostname}:{port}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"HTTP connection from {client_address}")
            client_thread = threading.Thread(target=handle_http_request, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down HTTP server...")
    finally:
        server_socket.close()


def load_table_data_from_db():
    table = [[""] * 7 for _ in range(7)]
    entries = session.query(TableData).all()
    for entry in entries:
        if 0 <= entry.row < 7 and 0 <= entry.column < 7:  # Bounds checking
            table[entry.row][entry.column] = entry.data
    return table


def save_table_data_to_db(row, col, value):
    if not (0 <= row < 7 and 0 <= col < 7):
        print(f"Invalid table coordinates: row={row}, col={col}")
        return
    entry = session.query(TableData).filter(TableData.row == row, TableData.column == col).first()
    if entry:
        if value == "":
            session.delete(entry)  # Remove entry if value is cleared
        else:
            entry.data = value
    else:
        if value != "":  # Only add non-empty values
            entry = TableData(row=row, column=col, data=value)
            session.add(entry)
    session.commit()


def broadcast_table_update():
    table_data = load_table_data_from_db()
    message = json.dumps({"type": "table_update", "data": table_data})
    with clients_lock:
        for client in connected_clients[:]:
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Failed to broadcast to client: {e}")
                connected_clients.remove(client)


def handle_tcp_client(client_socket, address):
    print(f"TCP connection from {address}")
    with clients_lock:
        connected_clients.append(client_socket)
    try:
        client_socket.sendall(json.dumps({"type": "table_update", "data": load_table_data_from_db()}).encode())
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            message = json.loads(data)
            if message["type"] == "update_table":
                row, col, value = message["row"], message["col"], message["value"]
                save_table_data_to_db(row, col, value)
                broadcast_table_update()
    except Exception as e:
        print(f"TCP client {address} disconnected: {e}")
    finally:
        with clients_lock:
            if client_socket in connected_clients:
                connected_clients.remove(client_socket)
        client_socket.close()


def start_tcp_server(hostname: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    print(f"TCP Server started on {hostname}:{port}")
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down TCP server...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    hostname = "localhost"
    http_port = 8080
    tcp_port = 8081

    threading.Thread(target=start_http_server, args=(hostname, http_port), daemon=True).start()
    start_tcp_server(hostname, tcp_port)
