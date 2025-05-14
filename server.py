import socket                # Import socket library for networking
import threading             # Import threading for handling multiple clients

clients = []      # List to store all connected chat clients

def handle_client(client_socket, addr):
    """
    Handles communication with a single client:
    - Receives the username.
    - Notifies others when the user joins.
    - Listens for messages from the client and broadcasts them.
    - Notifies others when the user leaves and cleans up.
    """
    try:
        username = client_socket.recv(1024).decode('utf-8')  # Receive username from client
        broadcast(f"{username} انضم إلى الدردشة!", client_socket)  # Notify others that user joined
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')  # Receive message from client
            if not message:    # If message is empty, client disconnected
                break
            broadcast(f"{username}: {message}", client_socket)  # Broadcast message to other clients
    except:
        pass    # Ignore any exceptions
    finally:
        clients.remove(client_socket)   # Remove client from list when disconnected
        broadcast(f"{username} غادر الدردشة", client_socket)  # Notify others that user left
        client_socket.close()           # Close client connection

def broadcast(message, sender_socket=None):
    """
    Sends a message to all connected clients except the sender.
    Removes clients that have disconnected.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))  # Send the message
            except:
                clients.remove(client)  # Remove client if sending fails

def start_server():
    """
    Starts the chat server:
    - Binds to port 5005 and listens for incoming connections.
    - For each new client, starts a new thread to handle communication.
    - Handles server shutdown gracefully.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
    server.bind(('0.0.0.0', 5005))         # Bind socket to all interfaces on port 5005
    server.listen()                        # Start listening for connections
    print("سيرفر الدردشة يعمل على المنفذ 5005...")  # Print server running message
    
    try:
        while True:
            client_socket, addr = server.accept()   # Accept new client connection
            clients.append(client_socket)           # Add client to the list
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))  # Create a thread for the client
            thread.start()                          # Start the client thread
    except KeyboardInterrupt:
        print("جارٍ إيقاف السيرفر...")             # Print message when stopping the server
    finally:
        server.close()                             # Close the server socket

if __name__ == "__main__":
    start_server()     # Start the server if the file is run directly
