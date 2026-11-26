"""One-connection TCP status receiver for a synthetic AMR socket lab.

No proprietary systems or real robot data are used. Bound to localhost by default.
"""

import argparse
import json
import socket

HOST = "127.0.0.1"
DEFAULT_PORT = 12000
MAX_MESSAGE_BYTES = 4096


def receive_line(connection: socket.socket) -> bytes:
    """Read one newline-delimited application message from a TCP byte stream."""
    collected = bytearray()
    while len(collected) < MAX_MESSAGE_BYTES:
        chunk = connection.recv(min(1024, MAX_MESSAGE_BYTES - len(collected)))
        if not chunk:
            raise ConnectionError("Peer closed before message delimiter")
        collected.extend(chunk)
        if b"\n" in collected:
            # This lab exchanges exactly one message per connection.
            return bytes(collected.split(b"\n", 1)[0])
    raise ValueError("Message too large")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic AMR TCP status receiver")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((HOST, args.port))
        listening_socket.listen(1)
        local_ip, local_port = listening_socket.getsockname()
        print(f"SERVER listening on {local_ip}:{local_port}", flush=True)

        # listen(1) configures the accept backlog; this lab deliberately accepts one client.
        connection, peer = listening_socket.accept()
        with connection:
            connection.settimeout(8)
            print(f"SERVER accepted TCP connection from {peer[0]}:{peer[1]}", flush=True)
            try:
                raw = receive_line(connection)
                message = json.loads(raw.decode("utf-8"))
                print(f"SERVER received application message: {message}", flush=True)
                if not isinstance(message, dict) or message.get("type") != "robot_status":
                    raise ValueError("Expected a robot_status JSON object")
                if message.get("robot_id") != "AMR-01" or message.get("status") != "mission_complete":
                    raise ValueError("Unexpected synthetic robot ID or status")
                reply = {
                    "type": "status_ack",
                    "robot_id": message["robot_id"],
                    "received_status": message["status"],
                    "accepted": True,
                }
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                reply = {"type": "error", "accepted": False, "reason": str(exc)}

            encoded = (json.dumps(reply, separators=(",", ":")) + "\n").encode("utf-8")
            connection.sendall(encoded)
            print(f"SERVER sent application response: {reply}", flush=True)
            print("SERVER closed client connection", flush=True)


if __name__ == "__main__":
    main()
