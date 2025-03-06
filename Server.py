import socket
import threading
import time
from threading import Semaphore, Lock

HOST = '127.0.0.1'
PORT = 5001
MAX_CONNECTIONS = 3
