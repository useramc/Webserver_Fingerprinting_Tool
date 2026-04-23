# Secure Web Server Fingerprinting Tool

##  Overview
This project is a web server fingerprinting system that detects the server type and version of target websites using HTTP/HTTPS banner grabbing.

It includes:
- Terminal-based client
- React frontend (fingerprint-ui)
- Secure Python backend using sockets and SSL

---

##  Architecture

React Frontend (fingerprint-ui)
        |
        v
Python Secure Server (Socket + SSL)
        |
        v
Target Websites (HTTP / HTTPS)

---

##  Features

- SSL-secured communication
- Multi-threaded server
- HTTP & HTTPS scanning
- Server detection (Apache, Nginx, IIS, etc.)
- Version extraction using regex
- Terminal + Web interface

---

##  Technologies Used

Frontend: React (fingerprint-ui)
Backend: Python
Networking: Socket Programming
Security: SSL/TLS
Concurrency: Multithreading

---

##  Project Structure

project/
│── server.py
│── client.py
│── cert.pem
│── key.pem
│
├── fingerprint-ui/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md

---

##  How It Works

Terminal Flow:
1. User enters URL
2. Client sends via socket
3. Server scans
4. Result displayed

Web Flow:
1. User enters URL in UI
2. Request sent to backend
3. Server scans
4. Result shown in UI

---

##  Data Flow

1. Input from user
2. Request sent to server
3. SSL connection established
4. Server performs scan
5. Headers extracted
6. Server + version detected
7. Response sent back
8. Output displayed

---

## 🧪 Sample Output

Enter target website: example.com

[+] Scanning...

Target   : example.com
Protocol : HTTPS
Server   : Nginx
Version  : 1.18.0

---

## Setup & Run

1. Generate SSL Certificate
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

2. Start Server
python3 server.py

3. Run Terminal Client
python3 client.py

4. Run React Frontend
cd fingerprint-ui
npm install
npm start

---

##  Key Concepts

Socket Programming:
socket.socket()
connect()
send()
recv()

SSL Encryption:
ssl.wrap_socket()

Multithreading:
threading.Thread()

Banner Grabbing:
HEAD / HTTP/1.1


##  Authors

CHINMAYI HEBBAR AM (PES2UG24CS134)
GUNAVATHI MI (PES2UG24CS172)
GAUTHAM L (PES2UG24CS171)

---

## ⭐ Note

For educational and ethical use only
