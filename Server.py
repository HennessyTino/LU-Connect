import socket
import threading
import time
import sqlite3
from threading import Semaphore, Lock
import datetime

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
    cursor.execute(''''
      CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')


def store_message(username, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)", (username, message, ts))
    connection.commit()
    connection.close()
 



def client_handler(client,address):