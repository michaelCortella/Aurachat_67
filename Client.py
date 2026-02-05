import socket
import time
import psutil
# 1. Creazione del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
address = ""
for iface, addrs in psutil.net_if_addrs().items():
            if iface.lower() == "ethernet":
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        address:str = addr.address

client_socket_UDP.bind((address,50402))
def get_server_address():
    while True:
        client_socket_UDP.sendto(f"{address}".encode(),("255.255.255.255",50402))
        data = client_socket_UDP.recvfrom(1024)[0].decode()
        if data != "":
            print(data)
            return data
        time.sleep(2)


client_socket.connect((get_server_address().strip(), 20405))
uscita = ""
while uscita != "EXIT":
    messaggio = input("Inserire il nuovo messaggio da mandare, digitare \"EXIT\" per uscire: ")

    uscita = messaggio
    # 3. Invio di un messaggio
    client_socket.send(messaggio.encode())
    print("messaggio inviato")
    print(messaggio)
    # 4. Ricezione risposta
    data = client_socket.recv(1024).decode()
    print("messaggio ricevuto")
    if data.lower() == "closed":
        break

    print(f"Risposta dal server: {data}")
    uscita = messaggio

# 5. Chiusura connessione
print("Socket chiuso")
input()
client_socket.close()