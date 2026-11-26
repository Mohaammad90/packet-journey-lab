"""Synthetic AMR client that sends one JSON message over a real TCP socket."""

import argparse
import json
import socket

HOST = "127.0.0.1"
DEFAULT_PORT = 12000


def receive_line(connection: socket.socket) -> bytes:
    response = bytearray()
    while len(response) < 4096:
        chunk = connection.recv(1024)
        if not chunk:
            raise ConnectionError("Server closed before response delimiter")
        response.extend(chunk)
        if b"\n" in response:
            return bytes(response.split(b"\n", 1)[0])
    raise ValueError("Response too large")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic AMR TCP socket client")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    request = {"type": "robot_status", "robot_id": "AMR-01", "status": "mission_complete"}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(8)
        client.connect((HOST, args.port))
        client_ip, client_port = client.getsockname()
        server_ip, server_port = client.getpeername()
        print(f"CLIENT TCP established: {client_ip}:{client_port} -> {server_ip}:{server_port}")
        raw = (json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8")
        client.sendall(raw)
        print(f"CLIENT sent {len(raw)} bytes of application data: {request}")
        response = json.loads(receive_line(client).decode("utf-8"))
        print(f"CLIENT received application response: {response}")
        if response.get("type") != "status_ack" or not response.get("accepted"):
            raise RuntimeError("Server did not accept the status update")
        print("CLIENT confirmed server processed the synthetic message")


if __name__ == "__main__":
    main()
