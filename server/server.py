import socket
import threading


# פונקציה לטיפול בכל לקוח
def handle_client(client_socket, client_address):
    print(f"New connection established with {client_address}")

    # תקשורת עם הלקוח
    while True:
        # קבלת הודעה מהלקוח
        message = client_socket.recv(1024).decode('utf-8')
        if not message:  # אם הלקוח סגר את החיבור
            break
        print(f"Received from {client_address}: {message}")

        # שליחת תשובה ללקוח
       # response = input("Enter message to send to client: ")
        #client_socket.send(response.encode('utf-8'))

    print(f"Closing connection with {client_address}")
    client_socket.close()


# פונקציה להפעלת השרת
def start_server():
    # יצירת סוקט (socket) חדש
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # הגדרת כתובת ה-IP והפורט להאזנה
    host = '127.0.0.1'  # IP המקומי (localhost)
    port = 12345  # הפורט שבו השרת יאזין

    # חיבור הסוקט לכתובת ופורט
    server_socket.bind((host, port))

    # הגדרת מספר החיבורים המקסימליים
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    # קבלת חיבורים מלקוחות
    while True:
        client_socket, client_address = server_socket.accept()

        # יצירת חוט חדש לכל לקוח שמתחבר
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    server_socket.close()


if __name__ == "__main__":
    start_server()