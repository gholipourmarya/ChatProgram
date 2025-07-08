# Chat_Programm

## 1. Executive Summary  
The **ChatApp** project is a simple and practical chat application developed in **Python**. Its goal is to create an environment for real-time communication between users. The app can serve as a foundation for more advanced chat systems.

---

## 2. Objective and Scope  

### Objective:
- Development of a basic real-time chat application

### Scope:
- Connecting multiple users within a local network  
- Sending and receiving text messages  
- Simple graphical user interface (GUI) with **Tkinter**

---

## 3. Technologies Used

- **Programming Language:** Python 3.12  
- **Libraries:**
  - `socket` for network communication  
    *(TCP server socket: `AF_INET`, `SOCK_STREAM`)*
  - `threading` for parallel connections  
  - `tkinter` for GUI (if used)  
  - `sys`, `os`, `select`, `errno` for system-level operations

---

## 4. Execution Files

- `main.py`  
- `server.py`  
- `client.py`  
- `header.py`

---

## 5. User Guide

1. Start the server (`server.py`)
2. Launch the client (`client.py`)
3. Enter a username
4. Send and receive messages via the GUI

---

## 6. Implemented Features

- Stable TCP network connection  
- Concurrent text chat between users  
- Multiple users connected simultaneously  

---

## 7. Future Enhancements

- User authentication (login/signup)  
- Storing messages in a database  
- End-to-end communication encryption  
- Web or mobile version of the chat app  

---

## 8.  Attachments

- `Flowerchart.png`  
- `Structure.png`  

---

## Notes

> This is a local-network-based chat application designed for learning and demonstration purposes. Future versions can include more advanced networking and security features.

![Flowerchart](https://github.com/user-attachments/assets/9d1974ee-78db-4319-a9c1-f2c13797b3f0)
![Structure](https://github.com/user-attachments/assets/dd5800af-fe9e-4b1f-82e6-d45b8a86a7cb)
