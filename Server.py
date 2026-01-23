import socket
import threading
from datetime import datetime
import time
import psutil

class Server():
    def __init__(self):
        for iface, addrs in psutil.net_if_addrs().items():
            if iface.lower() == "ethernet":
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        self.address:str = addr.address
        
    def discovery_response(self):
        socket_data,socket_address = self.server_socket_UDP.recvfrom(1024)
        self.server_socket_UDP.sendto(self.address.encode(), socket_address)

    def start(self):
        self.server_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket_UDP.bind(("", 20405))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.address, 20405))#finds the machines ip and connects it to port 60000
        self.server_socket.listen(5)#queues at most 5 clients
        self.active = True

    
    def discovery_handle(self):
        while self.active:
            threading.Thread(target=self.discovery_response,daemon=True).start()
    
    def shutdown(self): #todo
        pass

    def handle_client(self,client_socket):
        while self.active:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "TIME":
                client_socket.send(f"{datetime.now().strftime("%H:%M:%S")}".encode())
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
    server.discovery_handle()
    try:
        threading.Thread(target=server.accept_connection,daemon=True).start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
main()