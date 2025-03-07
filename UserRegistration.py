import sqlite3
import hashlib


DB_NAME = "users.db"


#! Initialize databse by creating the user table if it already doesnt exits
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        );   
    ''')
    conn.commit()
    conn.close()


#! Hash function to encrypt the password, based on the lectures from the course of Secure Cyber Systems
def hash_password(password):
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password_hash



def register_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return False, "Username already exists."
    
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()
    return True, "User registered successfully. \nYou can now chat. \nType 'exit' to disconnect.\n"




def login_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return False, "Username does not exist."
    
    stored_hash = row[0]
    computed_hash = hash_password(password)
    conn.close()

    if computed_hash == stored_hash:
        return True, "Login successful. \nYou can now chat. \nType 'exit' to disconnect.\n"
    else:
        return False, "Incorrect password."
    


