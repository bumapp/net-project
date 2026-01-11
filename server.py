import socket
import threading
import datetime

HOST = "192.168.0.53"
PORT = 50000

clients = {}


# Print time in any message
def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


# Send message to all connected users
def broadcast(message):
    for client in list(clients.keys()):
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            del clients[client]


# Handle clients socket
def handle_client(sock, addr):
    try:
        # First message from client
        username = sock.recv(1024).decode('utf-8')
        clients[sock] = username
        join_msg = f"[{timestamp()}] >> {username} joined the chat. Connected USERS: {list(clients.values())}  "
        broadcast(join_msg)  # Inform all connected users about a new one
        print(f"[+] {username} connected from {addr}")  # Logging

        while True:
            # Recive messages from clients and broadcast
            msg = sock.recv(1024)
            if not msg:
                break
            msg_text = msg.decode('utf-8')
            full_message = f"[{timestamp()}] >> {username}: {msg_text}"
            broadcast(full_message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Delete disconnected user and inform all connected users
        if sock in clients:
            left_user = clients[sock]
            del clients[sock]
            sock.close()
            leave_msg = f"[{timestamp()}] *** {left_user} left the chat. Connected USERS: {list(clients.values())} ***"
            broadcast(leave_msg)
            print(f"[-] {left_user} disconnected")  # Logging


# Main function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        sock, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(sock, addr))
        client_thread.start()


if __name__ == "__main__":
    start_server()
