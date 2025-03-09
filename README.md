
<!-- Table of Contents -->
# Table of Contents

- [About the Project](#about-the-project)
  * [Languages](#languages)
  * [Features](#features)
  * [Libraries](#libraries)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Run Locally](#run-locally)
  * [Deployment](#deployment)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)
  

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
<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites
- This prokect uses *brew* as package manager locally
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
  git clone https://github.com/Louis3797/awesome-readme-template.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  yarn install
```

Start the server

```bash
  yarn start
```


<!-- Deployment -->
### Deployment

To deploy this project run

```bash
  yarn deploy
```


<!-- Usage -->
## Usage

Use this space to tell a little more about your project and how it can be used. Show additional screenshots, code samples, demos or link to other resources.


```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```

<!-- Contact -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/Louis3797/awesome-readme-template](https://github.com/Louis3797/awesome-readme-template)


<!-- Acknowledgments -->
## Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Shields.io](https://shields.io/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#travel--places)
 - [Readme Template](https://github.com/othneildrew/Best-README-Template)
