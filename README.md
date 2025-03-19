
<!-- Table of Contents -->
# Table of Contents

- [About the Project](#about-the-project)
  * [Languages](#languages)
  * [Features](#features)
  * [Libraries](#libraries)
  * [Design Pattern](#design-pattern)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Run Locally](#run-locally)
- [Usage](#usage)
- [References](#references)
  

<!-- About the Project -->
## About the Project


<!-- TechStack -->
### Languages

  <summary>Client: </summary>
    <li><a href="https://www.python.org/">Python</a></li>


  <summary>Server: </summary>
    <li><a href="https://www.python.org/">Python</a></li>


  <summary>Database: </summary>
    <li><a href="https://www.sqlite.org">SQLite</a></li>

  <summary>GUI: </summary>
    <li><a href="https://docs.python.org/es/3.13/library/tkinter.html">TKinter</a></li>




<!-- Features -->
### Features

- Allows Users to register to LU-connect
- Allows Users to login into LU-connect
- Users can chat with other users simultaneously
- LU-Connect offers password encryption via SHA-256
- LU-Connect allows up to 3 connections at the same time
- The 4th connection will be put into a queue until a slot is available
- Client will play a "notification" sound when a message is received
- User information and messages will be stored in the "Lu-connect" database
- Lu-Connect implements a easy and simple to understand GUI

### Libraries
- Hashlib
- playsound
- datetime
- tkinter (GUI)


### Design Pattern

The design patter that I applied in this software was the "Mediator"  
this approach works well in this "chat" system since it is used as  
a single point of control for all the communication between clients.  
  
It manages all client connections in one place using "thread" safe locks.  
It also helps keep track of said clients and the distribuition of the messages.  
Instead of the clients communicating all of the messages go trough the mediator  
and the mediator broadcasts these messages to the other clients. It simiplifies  
the communication system.

The pattern is effective for this project since it imitates the real-word  
concept of a chat room with a moderator managing the communications with the clients.


<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites
- This project uses *brew* as package manager locally
- This project uses *pip3* as package manager inside the virtual enviroment

```bash
  python3 -m ensurepip
```

Install playsound to play notification sound when message is received

```bash
  pip install playsound
```

Install TKinter, this is used for the GUI

```bash
  brew install python-tk
```

<!-- Run Locally -->
### Run Locally

Clone the project

```bash
   git clone https://github.com/HennessyTino/LU-Connect.git
```

Go to the project directory

```bash
  cd LU-Connect
```

Run the Server

```bash
  python3 Server.py
```

In a separate terminal run the Client

```bash
  python3 Client.py
```

The GUI should pop up, and the software is ready for use.


<!-- Usage -->
## Usage

When the GUi pops up, the user will be prompted with the register or login option.  
If register is selected, the user will be asked to input a username and later on a password.  
Once the user information is inputed, the server will store the information in the LU-connect database.  
After registering the user is able to connect to the chat and start messaging right away.  
To exit the chat, the user must simply input ***"exit"*** and the connection will be terminated.  
If a old user returns, the option to ***"login"*** must be selected, and the user must input his information.  

Three users are able to connect simultaneously, if a 4th user wishes to connect, they will be placed  
in a waiting queue. To wait for the next slot to be availabe. Once the theres one, the user will  
be put the login/register process normally.



<!-- Contact -->
## Personal Information

Juan Valentin Toscano - **StudentID**: 39228436 - v.toscano@lancaster.ac.uk

Project Link: [https://github.com/HennessyTino/LU-Connect.git)

<!-- Acknowledgments -->
## References
- [README template] [https://github.com/Louis3797/awesome-readme-template.git)
- The encrypyion for this code was based on my Cyber Security Lectures
- The Server implementation was made using my Computer Network and Systems coursework as reference.







