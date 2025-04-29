import socket
import threading

clients = []      # قائمة لتخزين جميع عملاء الدردشة

def handle_client(client_socket, addr):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        broadcast(f"{username} انضم إلى الدردشة!", client_socket)
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{username}: {message}", client_socket)
    except:
        pass
    finally:
        clients.remove(client_socket)
        broadcast(f"{username} غادر الدردشة", client_socket)
        client_socket.close()

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5005))
    server.listen()
    print("سيرفر الدردشة يعمل على المنفذ 5005...")
    
    try:
        while True:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("جارٍ إيقاف السيرفر...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
