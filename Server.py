"""The server implementation for this project, was based on my Computer Network and Systems Coursework.
I used that coursework as a base guide to implement a socket server that can handle multiple clients at once."""




import socket
import threading
import time
import sqlite3
from threading import Semaphore, Lock
import datetime
from UserRegistration import register_user, login_user

HOST = '127.0.0.1'
PORT = 5001
MAX_CONNECTIONS = 3

#! using semaphore to limit the number of active connections
connection_limit = Semaphore(MAX_CONNECTIONS)

# This will be used later to put users in the waiting queue
waiting_queue = []


clients_lock = Lock()

#! Class that servers as a "Mediator", it stores client connections with their username
class LU_ConnectMediator:
    def __init__(self):
        self.clients = {}  
        self.lock = Lock()  
        

    def register_client(self, client, username):
        with self.lock:
            self.clients[client] = username

    def unregister_client(self, client):
        with self.lock:
            if client in self.clients:
                del self.clients[client]

    #! Broadcast function is part of "mediator" class it responsible for sending message to every client connected except the sender
    def broadcast(self, message, sender, notification = False):
        ts = datetime.datetime.now().strftime("%H:%M")
        with self.lock:
            if notification:
                formatted_msg = f"SYSTEM: [{ts}] {message}"
            else:
                sender_name = self.clients.get(sender, "Unknown")
                formatted_msg = f"[{ts}] {sender_name}: {message}"
            for client in self.clients:
                if client != sender:
                    try:
                        client.sendall(formatted_msg.encode())
                    except Exception as e:
                        print(f"[ERROR]: Error sending message: {e}")


mediator = LU_ConnectMediator()


#! initialize the messages database and create the table if it doesn't exist
def init_message_db():
    connection = sqlite3.connect("LUConnect.db")
    cursor = connection.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp TEXT
      )
    ''')
    connection.commit()
    connection.close()

#! Function that stores messages with a timestamp and the sending user's name
def store_message(username, message):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection = sqlite3.connect("LUConnect.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)", (username, message, ts))
    connection.commit()
    connection.close()

#! This function handles each individual client connection, and uses the "mediator" to manage comunication between clients
def client_handler(client, address): 
    username = ""  # Initialize username in case of early return
    print(f"[INFO]: Client {address} connected.")
    try:
        client.sendall(b"Welcome to LU-Connect! \nType 'register' or 'login': ")
        choice = client.recv(1024).lower().decode()
        if choice not in ("register", "login"):
            client.sendall(b"Invalid option. Disconnecting.")
            return

        client.sendall(b"Enter username: ")
        username = client.recv(1024).decode()
        client.sendall(b"Enter password: ")
        password = client.recv(1024).decode()

        if choice == "register":
            success, msg = register_user(username, password)
        else:
            success, msg = login_user(username, password)

        if not success:
            client.sendall(msg.encode())
            return

        with clients_lock:
            if username in mediator.clients.values():
                client.sendall(b"User already connected. Disconnecting.")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                return
            mediator.register_client(client, username)

        client.sendall(msg.encode())
        mediator.broadcast(f"{username} has connected to the chat.", client, notification = True)

        # Main communication loop: receive messages and broadcast them.
        while True:
            data = client.recv(1024)
            if not data:
                break
            text = data.decode()
            if text == "exit":
                mediator.broadcast(f"{username} has disconnected from the chat.", client, notification = True)
                break

            mediator.broadcast(text, client)
            store_message(username, text)

    finally:
        print(f"[INFO]: Client {address} ({username}) disconnected.")
        client.close()
        with clients_lock:
            mediator.unregister_client(client)
        connection_limit.release()  


#! Function to accept incoming client connections
def accept_connections(server):
    while True:
        client, addr = server.accept()
        print(f"[INFO] Incoming connection from {addr}")

        if connection_limit.acquire(blocking = False):
            accept_conn_thread = threading.Thread(target=client_handler, args = (client, addr))
            accept_conn_thread.daemon = True
            accept_conn_thread.start()
        else:
            client.sendall(b"Server is busy. Please wait...\n")
            waiting_queue.append((client, addr))

#! This function periodically checks the waiting queue and accepts connections
def waiting_queue_handler():
    while True:
        if waiting_queue:
            connection_limit.acquire()
            with clients_lock:
                client, addr = waiting_queue.pop(0)
            try:
                client.sendall(b"Slot available. Connecting now...\n")
            except Exception:
                # If sending fails, release the slot and continue
                connection_limit.release()
                continue
            waiting_queue_thread = threading.Thread(target=client_handler, args=(client, addr))
            waiting_queue_thread.daemon = True
            waiting_queue_thread.start()
        time.sleep(1)


#!Server Main
if __name__ == "__main__":
    #* Initialize the database for storing messages
    init_message_db()

    #* Create the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))  
    server.listen(5)
    print(f"[STARTED]: Server listening on {HOST}:{PORT}")

    #* Create thread to accept new connections
    accept_thread = threading.Thread(target=accept_connections, args=(server,))
    accept_thread.daemon = True
    accept_thread.start()

    #* Create thread to process the waiting queue of clients
    waiting_thread = threading.Thread(target=waiting_queue_handler)
    waiting_thread.daemon = True
    waiting_thread.start()

    #* Keep the server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is shutting down.")
        server.close()

