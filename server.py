import socket
import threading

# Server configurations
HOST = "127.0.0.1"  # Localhost
PORT = 12345        # Port to listen on

# Shared data
clients = []
choices = {}

def letsplay(choice1, choice2):
    # Function logic based on your earlier implementation
    if choice1 == choice2:
        return f"Both players chose {choice1}. It's a tie!"
    elif (choice1, choice2) in [("ROCK", "SCISSORS"), ("PAPER", "ROCK"), ("SCISSORS", "PAPER")]:
        return f"Player 1 ({choice1}) beats Player 2 ({choice2}). Player 1 wins!"
    else:
        return f"Player 2 ({choice2}) beats Player 1 ({choice1}). Player 2 wins!"

def handle_client(client_socket, client_id):
    global choices
    # Inform the players to wait until both are connected
    client_socket.send(b"Waiting for another player to join...\n")

    while True:
        if len(clients) == 2:  # When both players are connected, allow them to make a choice
            client_socket.send(b"Both players are connected! Type your choice (ROCK, PAPER, SCISSORS):\n")
            try:
                choice = client_socket.recv(1024).decode().strip().upper()
                if choice in ["ROCK", "PAPER", "SCISSORS"]:
                    choices[client_id] = choice
                    client_socket.send(b"Choice received. Waiting for the other player...\n")
                    if len(choices) == 2:
                        determine_winner()
                    break
                else:
                    client_socket.send(b"Invalid choice. Please choose ROCK, PAPER, or SCISSORS.\n")
            except Exception as e:
                print(f"Error with client {client_id}: {e}")
                break
        else:
            continue

def determine_winner():
    global choices
    player1, player2 = list(choices.keys())
    choice1, choice2 = choices[player1], choices[player2]

    # Call letsplay to determine the winner
    result = letsplay(choice1, choice2)

    # Send results to clients
    clients[0].send(result.encode() + b"\n")
    clients[1].send(result.encode() + b"\n")
    
    # Reset for next game
    choices.clear()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # Only allow 2 clients
    print(f"Server started on {HOST}:{PORT}. Waiting for players...")

    while len(clients) < 2:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_id = len(clients)
        print(f"Player {client_id} connected from {addr}.")
        threading.Thread(target=handle_client, args=(client_socket, client_id)).start()

if __name__ == "__main__":
    start_server()
