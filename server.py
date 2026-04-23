import socket
import ssl
import threading
import json
import re

HOST = "0.0.0.0"
PORT = 9999

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"


# -----------------------------
# Banner Grabbing
# -----------------------------
def http_banner(host):
    try:
        s = socket.socket()
        s.settimeout(4)
        s.connect((host, 80))

        req = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.send(req.encode())

        res = s.recv(4096).decode(errors="ignore")
        s.close()
        return res
    except:
        return None


def https_banner(host):
    try:
        context = ssl.create_default_context()

        s = socket.socket()
        conn = context.wrap_socket(s, server_hostname=host)
        conn.settimeout(4)

        conn.connect((host, 443))

        req = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        conn.send(req.encode())

        res = conn.recv(4096).decode(errors="ignore")
        conn.close()
        return res
    except:
        return None


# -----------------------------
# Detection
# -----------------------------
def detect_server(headers):
    h = headers.lower()

    if "nginx" in h: return "Nginx"
    if "apache" in h: return "Apache"
    if "iis" in h: return "Microsoft IIS"
    if "litespeed" in h: return "LiteSpeed"
    if "cloudflare" in h: return "Cloudflare"
    if "google" in h: return "Google Web Server"
    if "github" in h: return "GitHub Infrastructure"

    return "Unknown"


def extract_version(headers):
    match = re.search(r"\d+\.\d+(\.\d+)?", headers)
    return match.group(0) if match else "Unknown"


# -----------------------------
# Scan Logic
# -----------------------------
def scan_website(target):
    target = target.replace("http://", "").replace("https://", "").strip("/")

    res = https_banner(target)
    protocol = "HTTPS"

    if not res:
        res = http_banner(target)
        protocol = "HTTP"

    headers = res.split("\r\n\r\n")[0] if res else ""

    return {
        "target": target,
        "protocol": protocol,
        "server": detect_server(headers),
        "version": extract_version(headers)
    }


# -----------------------------
# Client Handler (THREAD)
# -----------------------------
def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")

    try:
        data = conn.recv(4096).decode()

        targets = json.loads(data)

        results = []

        for t in targets:
            r = scan_website(t)
            results.append(r)

        conn.send(json.dumps(results).encode())

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")

    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")


# -----------------------------
# Start Secure Server
# -----------------------------
def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"Secure Server running on port {PORT}...\n")

    while True:
        client_sock, addr = sock.accept()

        secure_conn = context.wrap_socket(client_sock, server_side=True)

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
