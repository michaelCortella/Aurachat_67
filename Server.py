import socket
import threading
from datetime import datetime

def handle_client(client_socket, client_address):
    print(f"Connessione da {client_address}")
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data == "TIME":
            client_socket.send(f"{datetime.now()}".encode())
        elif data == "NAME":
            client_socket.send(f"{socket.gethostname()}".encode())
        elif data == "EXIT":
            break
        else:
            print(f"Messaggio ricevuto: {data}")
            client_socket.send(f"Ciao {client_address[0]}, ho ricevuto il tuo messaggio!".encode())
    print(f"Connessione chiusa con {client_address}")
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)
print("Server in ascolto sulla porta 12345...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Server chiuso")
finally:
    server_socket.close()