
import socket
import threading
import sys
import Notification

HOST = '127.0.0.1'
PORT = 5001


def recieve_messages(client):
    while True:
        try: 
            message = client.recv(1024)
            if not message:
                break
            decoded_message = message.decode('utf-8')
            #* prints the received message and prompt.
            print("\r" + decoded_message + "\nYou: ", end="", flush=True)


            #! Defined prefixes to avoid playing notification sound at the wrong time.
            system_prefixes = ("Welcome", "Server busy", "Slot available", "Authentication", "Connected", "User", "has connected to the chat.", "has disconnected from the chat.")


            #* Ensures that notification sound is palyed if message does not contain a word from prefix list above
            if not any(prefix in decoded_message for prefix in system_prefixes):
                Notification.notification_sound("messagesound.wav")
        except Exception:
            break   


def send_messages(client):
    while True:
        message = input("You: ")
        if message == "exit":
            client.sendall(message.encode('utf-8'))
            break
        client.sendall(message.encode('utf-8'))


def authenticate(client):
    buffer = ""
    while "Welcome to LU-Connect" not in buffer:
        data = client.recv(1024).decode('utf-8')
        if not data:
            continue
        buffer += data
        print(data, end="")
    choice = input("")
    client.sendall(choice.encode('utf-8'))
    
    username_prompt = client.recv(1024).decode('utf-8')
    print(username_prompt, end="")
    username = input("")
    client.sendall(username.encode('utf-8'))
    
    password_prompt = client.recv(1024).decode('utf-8')
    print(password_prompt, end="")
    password = input("")
    client.sendall(password.encode('utf-8'))
    
    response = client.recv(1024).decode('utf-8')
    print(response, end="\nAuthentication successful.\n")
    if "successful" not in response:
        print("\nAuthentication failed. Exiting.")
        client.close()
        sys.exit(1)


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"[ERROR]: Connection Error: {e}")
        sys.exit(1)

    authenticate(client)

    receive_thread = threading.Thread(target = recieve_messages, args = (client,))
    receive_thread.start()

    send_thread = threading.Thread(target = send_messages, args = (client,))
    send_thread.start()


    send_thread.join()

    try:
        client.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    client.close()


    receive_thread.join()  

