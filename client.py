import socket

# Client configurations
HOST = "127.0.0.1"  # Server address
PORT = 12345        # Server port

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print("Connected to the server. Waiting for instructions...\n")
    while True:
        message = client.recv(1024).decode()
        if message:
            print(message)
        if "Type your choice" in message:
            choice = input("Your choice: ").strip().upper()
            client.send(choice.encode())
        if "wins!" in message or "tie" in message:
            break  # Game over, close connection

    print("Game over. Closing connection.")
    client.close()

if __name__ == "__main__":
    start_client()
