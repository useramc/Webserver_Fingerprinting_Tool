from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import ssl
import re

app = Flask(__name__)
CORS(app)

def http_banner(host, port=80):

    try:
        s = socket.socket()
        s.settimeout(4)

        s.connect((host, port))

        request_data = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.send(request_data.encode())

        response = s.recv(4096).decode(errors="ignore")

        s.close()

        return response

    except:
        return None



def https_banner(host, port=443):

    try:
        context = ssl.create_default_context()

        conn = context.wrap_socket(socket.socket(), server_hostname=host)
        conn.settimeout(4)

        conn.connect((host, port))

        request_data = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        conn.send(request_data.encode())

        response = conn.recv(4096).decode(errors="ignore")

        conn.close()

        return response

    except:
        return None


def extract_server(response):

    if not response:
        return ""

    headers = response.split("\r\n\r\n")[0]

    return headers



def extract_version(header_text):

    if not header_text:
        return "Unknown"

   
    match = re.search(r"\d+\.\d+(\.\d+)?", header_text)

    if match:
        return match.group(0)

    return "Unknown"

def detect_server(headers):

    h = headers.lower()

    if "nginx" in h:
        return "Nginx"

    if "apache" in h:
        return "Apache"

    if "iis" in h:
        return "Microsoft IIS"

    if "litespeed" in h:
        return "LiteSpeed"

    if "cloudflare" in h or "cf-ray" in h:
        return "Cloudflare"

    if "gws" in h or "google" in h:
        return "Google Web Server"

    if "github" in h:
        return "GitHub Infrastructure"

    if "fastly" in h:
        return "Fastly CDN"

    if "akamai" in h:
        return "Akamai CDN"

    return "Unknown"


def scan_website(host):

    response = https_banner(host)
    protocol = "HTTPS"

    if not response:
        response = http_banner(host)
        protocol = "HTTP"

    headers = extract_server(response)

    server_type = detect_server(headers)
    version = extract_version(headers)

    return {
        "target": host,
        "protocol": protocol,
        "server": server_type,
        "version": version
    }


@app.route("/scan", methods=["POST"])
def scan():

    data = request.json
    targets = data.get("targets", [])

    results = []

    for target in targets:
        result = scan_website(target)
        results.append(result)

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)