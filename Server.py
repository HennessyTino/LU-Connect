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

#This is going to be used later to put users in the waiting queue
waiting_queue = []

#Global list of clients and a dictionary to map sockets to usernames
clients = []
client_names = {}
clients_lock = Lock()


#! initialize the messages database and create the table if it doesnt exit
def init_message_db():
    connection = sqlite3.connect("messages.db")
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

#! Function that stores the messages, with a timestamp and the name of the user that sent said message
def store_message(username, message):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)", (username, message, ts))
    connection.commit()
    connection.close()



"""! broadcast function that broadcasts messages to all connected clients, exception of sender of course. With timestamp and username of the client that sent the message"""
def broadcast(message, sender, notification = False):
    ts = datetime.datetime.now().strftime("%H:%M")
    if notification:
        formatted_msg = f"SYSTEM: [{ts}] {message.decode()}"
    else:
        user = client_names.get(sender, "Unknown")
        formatted_msg = f"[{ts}] {user}: {message.decode()}"

    with clients_lock:
        for client in clients:
            if client != sender:
                try:
                    client.sendall(formatted_msg.encode())
                except Exception as e:
                    print(f"[ERROR]: Error sending message:", e)
    



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
            if username in client_names.values():
                client.sendall(b"User already connected. Disconnecting.")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                return
            clients.append(client)
            client_names[client] = username

        client.sendall(msg.encode())

        broadcast(f"{username} has connected to the chat.".encode(), client, notification=True)


        #! This is the main communication loop, server only recieves messages and broadcasts them
        while True:
            data = client.recv(1024)
            if not data:
                break
            text = data.decode()
            if text == "exit":
                broadcast(f"{username} has disconnected from the chat.".encode(), client, notification=True)
                break

            #This broadcasts the message to the other connected clients
            broadcast(data, client)
            #This stores the message in the "messages.db" database
            store_message(username, text)


    finally:
        print(f"[INFO]: Client {address} ({username}) disconnected.")
        client.close()
        with clients_lock:
            if client in clients:
                clients.remove(client)
            client_names.pop(client, None)
        connection_limit.release() #! remove client from semaphore to allow a new connection



#! Function to accpet incoming clien connections
def accept_connections(server):
    while True:
        client, addr = server.accept()
        print(f"[INFO] Incoming connection forom {addr}")

        if connection_limit.acquire(blocking = False):
            accept_conn_thread = threading.Thread(target = client_handler, args = (client, addr))
            accept_conn_thread.daemon = True
            accept_conn_thread.start()

        else:
            client.sendall(b"Server is busy. Please  wait...\n")
            waiting_queue.append((client, addr))
            


#! This function periodicaly checks the waiting queue and accepts connections
def waiting_queue_handler():
    while True:
        if waiting_queue:
            connection_limit.acquire()
            client, addr = waiting_queue.pop(0)
            client.sendall(b"Slot available. Connecting now...\n")
            waiting_queue_thread = threading.Thread(target = client_handler, args = (client, addr))
            waiting_queue_thread.daemon = True
            waiting_queue_thread.start()
        time.sleep(1)



if __name__ == "__main__":
    #* Initialize the db for storing messages
    init_message_db()

    #* Create the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT)) #bind server to specific host and port
    server.listen(5)
    print(f"[STARTED]: Server listening on {HOST}:{PORT}")

    #* Create thread to accept new connections
    accept_thread = threading.Thread(target = accept_connections, args = (server,))
    accept_thread.daemon = True 
    accept_thread.start()

    #* Create thread to process the queue of waiting clients
    waiting_thread = threading.Thread(target = waiting_queue_handler)
    waiting_thread.daemon = True
    waiting_thread.start()


    #* Keep the server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is shutting down.")
        server.close()