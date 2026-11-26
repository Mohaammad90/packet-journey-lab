# AMR Socket Lab — Python TCP Client/Server

This is a **real localhost TCP exchange** using a fictional mobile robot and fleet service. It is a teaching experiment, not robot-control software.

## The protocol

```text
AMR-01 Python client                      Fleet Python server
127.0.0.1:<ephemeral>                     127.0.0.1:12000
        |                                       |
        +---------- TCP connect() ------------>|
        +----- robot_status JSON + '\\n' ----->|
        |<------ status_ack JSON + '\\n' ------+
```

The server uses `bind()`, `listen()` and `accept()`. The client uses `connect()`. Both programs use `sendall()` and `recv()` on a **TCP byte stream**, with newline framing for one message per connection.

## Run it

Python 3.9+; no third-party dependencies.

From the repository root, run in **Terminal 1**:

```bash
python3 labs/tcp-socket/server.py
```

Then in **Terminal 2**:

```bash
python3 labs/tcp-socket/client.py
```

The test creates and closes a server for **one** client. To repeat it, restart the server.

## Automated test

```bash
python3 -m unittest discover -s labs/tcp-socket/tests -v
```

The test starts a localhost server on an OS-assigned port, runs the client as a separate process, and verifies application acceptance. See [sample output](demo-output.txt).

## Interactive browser visualization

Open [`index.html`](index.html) or [the live demo on yasen.engineer](https://www.yasen.engineer/demos/amr-socket-lab/index.html). This is a **simulation** of TCP events; browsers cannot open arbitrary raw TCP sockets. Actual TCP communications take place only in the Python code.

## What to learn

1. The **listening socket** awaits new clients; `accept()` returns a **connected socket**.
2. TCP transports an ordered stream of bytes, not independent application messages.
3. TCP transport ACKs are **not** acknowledgments that the server application has accepted a request.
4. An application-level `status_ack` proves this example server parsed and accepted the synthetic record.

## Limits

Only one loopback client/server exchange is tested. No routing, UDP, DNS, TLS, packet captures, real AMRs, or real factory systems have been demonstrated.

See [the repository architecture](../../docs/architecture.md) and [evidence register](../../docs/evidence.md).
