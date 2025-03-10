import socket
import threading
import json

from models.user import User
from models.db.db import get_session, init_db

session = get_session()
init_db()

# Simulated table data for streaming
table_data = [[""] * 7 for _ in range(7)]
connected_clients = []
clients_lock = threading.Lock()


# Original HTTP handling logic moved into a function
def handle_http_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()
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
                    user_id = route_parameters[0]
                    user = session.query(User).filter(User.id == user_id).first()
                    if data["username"] is not None:
                        user.username = data["username"]
                    if data["password"] is not None:
                        user.password = data["password"]
                    session.commit()
                    return json.loads(user.__repr__()), 200

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
                    try:
                        user = session.query(User).filter(User.username == str(data['username']),
                                                          User.password == str(data['password'])).first()
                        return json.loads(user.__repr__()), 200
                    except:
                        return {'error': 'Not Found',
                                'reason': f"User with username {data['username']} not found in the db. Password might be wrong"}, 404

                if method == "POST" and 'user' in path:
                    data = extract_body_from_request(request)
                    new_user = User(username=data['username'], password=data['password'])
                    session.add(new_user)
                    session.commit()
                    return json.loads(new_user.__repr__()), 200

                return [{"error": "Not Found"}], 404
            except Exception as err:
                session.rollback()
                return [{"error": "Bad Request", "reason": str(err)}], 400

        response_body, status_code = handle_routing(request)
        response_body_json = json.dumps(response_body)
        status_message = "OK" if status_code == 200 else "Error"
        response = (f"HTTP/1.1 {status_code} {status_message}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(response_body_json)}\r\n\r\n"
                    f"{response_body_json}")
        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling HTTP request: {e}")
    finally:
        client_socket.close()


def start_http_server(hostname: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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


# TCP Server for Table Streaming
def broadcast_table_update():
    message = json.dumps({"type": "table_update", "data": table_data})
    with clients_lock:
        for client in connected_clients[:]:
            try:
                client.sendall(message.encode())
            except:
                connected_clients.remove(client)


def handle_tcp_client(client_socket, address):
    print(f"TCP connection from {address}")
    with clients_lock:
        connected_clients.append(client_socket)
    client_socket.sendall(json.dumps({"type": "table_update", "data": table_data}).encode())
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            message = json.loads(data)
            if message["type"] == "update_table":
                row, col, value = message["row"], message["col"], message["value"]
                table_data[row][col] = value
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

    # Start HTTP server in a thread
    threading.Thread(target=start_http_server, args=(hostname, http_port), daemon=True).start()
    # Start TCP server in the main thread
    start_tcp_server(hostname, tcp_port)
