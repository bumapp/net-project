import socket
import threading

HOST = "192.168.0.53"  # Server IP address
PORT = 50000  # Server port


# Receive messages from connected users
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                print("\r" + msg + "\n> ", end="")
        except Exception as e:
            print(f"\nError: {e}")
            print("\nDisconnected from server")  # Handle errors
            sock.close()
            break


# Main function
def start_client():
    username = input("Enter username: ")  # Connect to the chat with your name
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))  # Connect to the server
        print("Connected to chat server!")
        print("Type quit to exit.")
    except ConnectionRefusedError:  # Handle errors according to type of error
        print("Connection error or refused")
        return
    except TimeoutError:
        print("Connection timed out — server unreachable.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    client.send(username.encode('utf-8'))
    thread = threading.Thread(target=receive_messages, args=(client,))  # Threads for receiving and sending messages
    thread.start()

    while True:
        msg = input(" ")
        if msg.lower() == "quit":  # Type "quit" to disconnect from the chat
            break
        try:
            client.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Send Error: {e}")
            break

    client.close()


if __name__ == "__main__":
    start_client()
