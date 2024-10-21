import socket
import json
import threading

def get_server_ip():
    while True:
        ip = input("Enter server IP (or press Enter for localhost): ").strip()
        if ip == "":
            return "127.0.0.1"  # localhost
        elif ip.count(".") == 3 and all(0 <= int(num) < 256 for num in ip.split(".")):
            return ip
        else:
            print("Invalid IP address. Please try again.")

PORT = 12345
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_msg():
    while True:
        try:
            message_bytes = client.recv(1024)
            if not message_bytes:
                break
            
            message = json.loads(message_bytes.decode(FORMAT))

            if message.get('type') == 'message':
                print(f"{message.get('from')}: {message.get('message')}")
            elif message.get('type') == 'system':
                print(f"System: {message.get('message')}")

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_msg(message):
    try:
        message_json = json.dumps(message)
        message_bytes = message_json.encode(FORMAT)
        client.send(message_bytes)
    except Exception as e:
        print(f"Error sending message: {e}")

def connect_to_server(server_ip):
    try:
        client.settimeout(10)  # Set a timeout of 10 seconds
        client.connect((server_ip, PORT))
        client.settimeout(None)  # Remove the timeout after connection
        print(f"Connected to server at {server_ip}")
        return True
    except socket.timeout:
        print(f"Connection attempt timed out. Please check if the server is running and the IP is correct.")
    except ConnectionRefusedError:
        print(f"Connection was refused. Please check if the server is running and the IP is correct.")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
    return False

def init_client():
    server_ip = get_server_ip()
    if not connect_to_server(server_ip):
        return

    name = input("Enter your name: ")
    send_msg({'type': 'join', 'name': name})

    receive_thread = threading.Thread(target=receive_msg)
    receive_thread.start()

    print("Commands: 'connect <username>' to start chat, 'dis' to disconnect, 'quit' to exit")

    while True:
        message = input()
        if message.lower() == 'dis':
            send_msg({'type': 'disconnect'})
            print("Disconnected from the current user.")
        elif message.lower() == 'quit':
            send_msg({'type': 'disconnect'})
            print("Disconnected from the server.")
            break
        elif message.lower().startswith('connect '):
            target = message.split(' ', 1)[1]
            send_msg({'type': 'connect', 'target': target})
        else:
            send_msg({'type': 'message', 'message': message})

    client.close()

if __name__ == '__main__':
    init_client()
