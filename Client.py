import socket
import threading
import sys
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import Notification

HOST = '127.0.0.1'
PORT = 5001

# Pre-authentication function run in terminal before GUI loads.
def pre_auth(sock):
    # Retrieve first message from server.
    data = sock.recv(1024).decode('utf-8')
    if "Server is busy" in data:
        print(data.strip())
        # Wait until "Slot available" is received.
        while True:
            data = sock.recv(1024).decode('utf-8')
            print(data.strip())
            if "Slot available" in data:
                break
        # After slot available, read the welcome message.
        welcome_msg = sock.recv(1024).decode('utf-8')
        # Do not print the welcome message; return it instead.
        return welcome_msg
    else:
        return data

class LU_ConnectGUI:
    #! Innit mainly for GUI, it generates the GUI and the options to customize it
    def __init__(self, master, sock, welcome_msg="", theme = None):
        self.master = master
        self.master.title("LU-Connect Chat")
        self.sock = sock
        self.notifications_enabled = True
        
        self.theme = theme or {
            "chat_bg": "#4F4F4F",
            "chat_font": ("San Francisco", 12),  
            "entry_bg": "#4F4F4F",
            "entry_font": ("San Francisco", 12)
        }
        
        
        self.chat_area = scrolledtext.ScrolledText(master, wrap = tk.WORD, bg = self.theme["chat_bg"], font = self.theme["chat_font"], fg="white")
        self.chat_area.pack(padx = 10, pady = 10, fill=tk.BOTH, expand = True)
        self.chat_area.config(state = tk.DISABLED)
        
        self.entry_field = tk.Entry(master, bg = self.theme["entry_bg"], font = self.theme["entry_font"], fg = "white", width = 50)
        self.entry_field.pack(padx = 10, pady = 10, anchor = "w")  
        self.entry_field.bind("<Return>", self.send_message)
        
        
        if welcome_msg:
            self.update_chat_area(welcome_msg.strip())
        
       
        self.authenticate()

        #! Thread to start listening for messages to receive
        threading.Thread(target=self.receive_messages, daemon = True).start()


    #! Function to do authentication, sends the info to the server,
    def authenticate(self):
        choice = simpledialog.askstring("Authentication", "Type 'register' or 'login':")
        self.sock.sendall(choice.encode('utf-8'))
    
        username_prompt = self.sock.recv(1024).decode('utf-8')
        if "Invalid option" in username_prompt:
            self.update_chat_area(username_prompt.strip())
            self.sock.close()
            self.master.after(1000, lambda: (self.master.quit(), sys.exit(0)))
            return
        self.update_chat_area(username_prompt.strip())
    
        username = simpledialog.askstring("Authentication", "Enter username:")
        self.sock.sendall(username.encode('utf-8'))
    
        password_prompt = self.sock.recv(1024).decode('utf-8')
        if "Invalid option" in password_prompt:
            self.update_chat_area(password_prompt.strip())
            self.sock.close()
            self.master.after(1000, lambda: (self.master.quit(), sys.exit(0)))
            return
        self.update_chat_area(password_prompt.strip())
    
        password = simpledialog.askstring("Authentication", "Enter password:", show = "*")
        self.sock.sendall(password.encode('utf-8'))
    
        response = self.sock.recv(1024).decode('utf-8')
        self.update_chat_area(response.strip())
        if "successful" not in response:
            self.update_chat_area("Authentication failed. Exiting.")
            self.sock.close()
            self.master.after(1000, lambda: (self.master.quit(), sys.exit(0)))
    
    #! Function that listens to incoming messages and makes sure that the notification sound does not play in the wrong message like "welcome" message
    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024)
                if not message:
                    break
                decoded_message = message.decode('utf-8')
                self.update_chat_area(decoded_message)
                
                # Defined prefixes to avoid playing notification sound unnecessarily.
                system_prefixes = ("Welcome", "Server busy", "Slot available", "Authentication", "Connected", "User", "has connected to the chat.", "has disconnected from the chat.")
                if self.notifications_enabled and not any(prefix in decoded_message for prefix in system_prefixes):
                    Notification.notification_sound("messagesound.wav")
            except Exception:
                break

    def send_message(self, event = None):
        message = self.entry_field.get()
        if message.lower() == "/mute":
            self.notifications_enabled = False
            self.update_chat_area("Notifications muted.")
            self.entry_field.delete(0, tk.END)
            return
        elif message.lower() == "/unmute":
            self.notifications_enabled = True
            self.update_chat_area("Notifications unmuted.")
            self.entry_field.delete(0, tk.END)
            return
        
        if message.strip() == "exit":
            self.sock.sendall(message.encode('utf-8'))
            self.sock.close()
            self.master.quit()  # Terminate GUI
            import sys
            sys.exit(0)
        else:
            self.sock.sendall(message.encode('utf-8'))
            self.update_chat_area("You: " + message)
            self.entry_field.delete(0, tk.END)

    def update_chat_area(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"[ERROR]: Connection Error: {e}")
        sys.exit(1)
    
    
    welcome_message = pre_auth(sock)
    root = tk.Tk()
    client = LU_ConnectGUI(root, sock, welcome_message)
    root.protocol("WM_DELETE_WINDOW", lambda: (sock.sendall("exit".encode('utf-8')), sock.close(), root.quit(), sys.exit(0)))
    root.mainloop()

