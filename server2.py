from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import ssl
import re
import json
import threading

app = Flask(__name__)
CORS(app)

# 🔥 Shared storage (IMPORTANT)
shared_results = []

# -----------------------------
# SCANNER LOGIC (same as yours)
# -----------------------------
def http_banner(host):
    try:
        s = socket.socket()
        s.settimeout(8)
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
        conn.settimeout(8)

        conn.connect((host, 443))

        req = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        conn.send(req.encode())

        res = conn.recv(4096).decode(errors="ignore")
        conn.close()
        return res
    except:
        return None


def extract_version(headers):
    match = re.search(r"\d+\.\d+(\.\d+)?", headers)
    return match.group(0) if match else "Unknown"


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
# SOCKET SERVER
# -----------------------------
def handle_socket_client(conn):
    global shared_results

    try:
        data = conn.recv(4096).decode()
        targets = json.loads(data)

        results = []

        for t in targets:
            r = scan_website(t)
            results.append(r)
            shared_results.append(r)   # 🔥 STORE

        conn.send(json.dumps(results).encode())

    except Exception as e:
        print("Socket error:", e)

    finally:
        conn.close()


def socket_server():
    HOST = "0.0.0.0"
    PORT = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Socket server running on 9999...")

    while True:
        conn, addr = server.accept()
        print("Socket client:", addr)
        handle_socket_client(conn)

# -----------------------------
# FLASK API
# -----------------------------
@app.route("/scan", methods=["POST"])
def api_scan():
    global shared_results

    data = request.json
    targets = data.get("targets", [])

    results = []

    for t in targets:
        r = scan_website(t)
        results.append(r)
        shared_results.append(r)   # 🔥 STORE

    return jsonify(results)


# 🔥 NEW: Get ALL results
@app.route("/results", methods=["GET"])
def get_results():
    return jsonify(shared_results)


# -----------------------------
# START BOTH SERVERS
# -----------------------------
if __name__ == "__main__":
    threading.Thread(target=socket_server, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
