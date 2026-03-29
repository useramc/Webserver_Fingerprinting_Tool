import socket
import json

SERVER_IP = "10.1.0.30"   
PORT = 9999


def get_targets():
    targets = []

    print("Enter websites (type 'done' to stop):")

    while True:
        t = input("Target: ")
        if t.lower() == "done":
            break
        if t:
            targets.append(t)

    return targets


def send_request(targets):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    client.send(json.dumps(targets).encode())

    response = client.recv(4096).decode()

    client.close()

    return json.loads(response)


def display(results):
    print("\nResults:\n")

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
