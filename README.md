# Chat Application 💬
A simple client-server chat application implemented in Python using sockets, allowing users to connect, send messages, and communicate in real-time.

## Features
- Multi-User Support 🫂
  - Allows multiple users to connect to the server simultaneously.
  - Users can join and leave without affecting other connections.
- User Registration
  - Users can identify themselves by entering a username when they join.
  - Ensures that each username is unique across sessions.
- Direct Messaging 📲
  - Users can initiate a private chat with another user by using the command connect <username>.
  - Messages are sent directly to the targeted user without broadcasting to all connected clients.

## Usage
- Running the Server
    -In the terminal, navigate to the directory where the server code is saved.
    -python server.py
    -The server will start and listen for incoming connections.

- Running the Client
    -Open another terminal or command prompt.
    -Navigate to the directory where the client code is saved.
    -python client.py
- Follow the prompts to enter the server IP address (or press Enter for localhost) and your name.
## Commands
- Connect to a user: connect <username>
- Disconnect from the current user: dis
- Quit the chat: quit



## Requirements
- Python 3.x
- socket (included with Python standard library)
- json (included with Python standard library)
- threading (included with Python standard library)
