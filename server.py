import socket
import threading
import json

SERVER_IP = '0.0.0.0'
PORT = 12345
SERVER_ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

connected_clients = {}
client_connections = {}

def send_msg(message, conn):
    try:
        message_json = json.dumps(message)
        message_bytes = message_json.encode(FORMAT)
        conn.send(message_bytes)
    except Exception as e:
        print(f"Error sending message: {e}")

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    name = None
    while True:
        try:
            message_bytes = conn.recv(1024)
            if not message_bytes:
                break

            message = json.loads(message_bytes.decode(FORMAT))
            msg_type = message.get('type')

            if msg_type == 'join':
                name = message.get('name')
                connected_clients[name] = conn
                print(f"{name} joined the chat from {addr}")
                send_msg({'type': 'system', 'message': f'Welcome, {name}! Type "connect <username>" to chat with someone.'}, conn)

            elif msg_type == 'connect':
                target_name = message.get('target')
                if target_name in connected_clients:
                    client_connections[name] = target_name
                    client_connections[target_name] = name
                    send_msg({'type': 'system', 'message': f'Connected to {target_name}'}, conn)
                    send_msg({'type': 'system', 'message': f'{name} has connected to you'}, connected_clients[target_name])
                else:
                    send_msg({'type': 'system', 'message': f'User {target_name} not found'}, conn)

            elif msg_type == 'message':
                if name in client_connections:
                    target_name = client_connections[name]
                    target_conn = connected_clients[target_name]
                    send_msg({'type': 'message', 'from': name, 'message': message.get('message')}, target_conn)
                else:
                    send_msg({'type': 'system', 'message': 'You are not connected to anyone. Use "connect <username>" first.'}, conn)

            elif msg_type == 'disconnect':
                if name in client_connections:
                    target_name = client_connections[name]
                    del client_connections[name]
                    del client_connections[target_name]
                    send_msg({'type': 'system', 'message': f'Disconnected from {target_name}'}, conn)
                    send_msg({'type': 'system', 'message': f'{name} has disconnected from you'}, connected_clients[target_name])
                else:
                    send_msg({'type': 'system', 'message': 'You were not connected to anyone.'}, conn)

        except Exception as e:
            print(f"Error handling client {name}: {e}")
            break

    if name:
        del connected_clients[name]
        if name in client_connections:
            target_name = client_connections[name]
            del client_connections[name]
            del client_connections[target_name]
            send_msg({'type': 'system', 'message': f'{name} has disconnected'}, connected_clients[target_name])
        print(f"{name} left the chat")
    conn.close()

def init_server():
    server.listen()
    print(f"[Server] Starting Server On: {SERVER_ADDR}")
    print(f"[Server] Local IP: {socket.gethostbyname(socket.gethostname())}")
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[Server] Active Connections: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("[Server] Shutting down.")
            break
        except Exception as e:
            print(f"[Server] Error: {e}")

if __name__ == '__main__':
    init_server()