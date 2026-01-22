import socket
import threading
from datetime import datetime
import time
import psutil

class Server():
    def __init__(self):
        
        pass
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("172.16.7.205", 20405))#finds the machines ip and connects it to port 60000
        print(self.server_socket)
        self.server_socket.listen(5)#queues at most 5 clients
        self.active = True
    
    def shutdown(self):
        pass

    def handle_client(self,client_socket):
        while self.active:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "TIME":
                client_socket.send(f"{datetime.now().strftime("%h:%m:%s")}".encode())
            elif data == "NAME":
                client_socket.send(f"{socket.gethostname()}".encode())
            elif data == "EXIT":
                break
            else:
                client_socket.send("comando non riconosciuto".encode())
        client_socket.shutdown()
        client_socket.close()

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept() #accepts conection
        client_socket.settimeout(120)#sets timeout value
        client_thread = threading.Thread(target=self.handle_client, args=(client_socket,),daemon=True)#makes the server multiclient
        client_thread.start()

def main():
    server = Server()
    server.start()
    print("server in ascolto")
    try:
        threading.Thread(target=server.accept_connection,daemon=True).start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
main()