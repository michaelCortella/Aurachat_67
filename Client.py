import socket

# 1. Creazione del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
def get_server_address():
    client_socket_UDP.connect(("255.255.255.255",20405))
    client_socket_UDP.sendto("DISCOVER_MESSAGE".encode(),("255.255.255.255",20405))
    return client_socket_UDP.recvfrom(1024)

# 2. Connessione al server (IP localhost e porta 12345)
client_socket.connect((get_server_address(), 12345))

uscita = ""
messaggio = "Ciao server, sono il client!"
client_socket.send(messaggio.encode())
data = client_socket.recv(1024).decode()

while uscita != "EXIT":
    messaggio = input("Inserire il nuovo messaggio da mandare, digitare \"EXIT\" per uscire: ")

    uscita = messaggio
    # 3. Invio di un messaggio
    client_socket.send(messaggio.encode())

    # 4. Ricezione risposta
    data = client_socket.recv(1024).decode()
    if data.lower() == "closed":
        break

    print(f"Risposta dal server: {data}")
    uscita = messaggio

# 5. Chiusura connessione
print("Socket chiuso")
input()
client_socket.close()