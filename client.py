import socket
import ssl
import json

SERVER_IP = "10.1.22.153"   # change if different device 
PORT = 9999


def get_targets():
    targets = []

    print("Enter websites (type 'done' to stop):")

    while True:
        t = input("Target: ").strip()
        if t.lower() == "done":
            break
        if t:
            targets.append(t)

    return targets


def send_request(targets):
    context = ssl._create_unverified_context()   

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = context.wrap_socket(sock, server_hostname=SERVER_IP)

    client.connect((SERVER_IP, PORT))

    client.send(json.dumps(targets).encode())

    response = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        response += chunk

    client.close()

    return json.loads(response.decode())


def display(results):
    print("\n=== Scan Results ===\n")

    for r in results:
        print(f"Target   : {r['target']}")
        print(f"Protocol : {r['protocol']}")
        print(f"Server   : {r['server']}")
        print(f"Version  : {r['version']}")
        print("-" * 40)


if __name__ == "__main__":
    targets = get_targets()
    results = send_request(targets)
    display(results)
