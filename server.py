import socket
import threading
from config import HOST, PORT

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(client):
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            # 🔒 Server DOES NOT decrypt (E2EE simulation)
            broadcast(data, client)

        except:
            break

    remove_client(client)

def remove_client(client):
    if client in clients:
        clients.remove(client)
        client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"[CONNECTED] {addr}")

        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    start_server()