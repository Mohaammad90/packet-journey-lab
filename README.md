# Packet Journey Lab

A public, reproducible network engineering lab using **synthetic** application traffic. Built around an independently tested TCP socket experiment, with a larger routed Linux network laboratory planned.

**Engineering portfolio:** [yasen.engineer](https://www.yasen.engineer/)  
**Interactive TCP teaching demo:** [Launch the browser simulation](https://www.yasen.engineer/demos/amr-socket-lab/index.html)  
**Technical case study:** [AMR Socket Lab](https://www.yasen.engineer/projects/amr-socket-lab.html)

## Verified: TCP Socket Lab

Two separate Python processes communicate over an actual TCP loopback connection using newline-delimited JSON. A fictional robot client sends `robot_status`; a server parses it and responds with a separate application-level `status_ack`.

**Run the automated end-to-end test** from the repository root:

```bash
python3 -m unittest discover -s labs/tcp-socket/tests -v
```

**Run the client and server** in separate terminals, from the repository root:

```bash
# Terminal 1
python3 labs/tcp-socket/server.py
```

```bash
# Terminal 2
python3 labs/tcp-socket/client.py
```

The server accepts one client and exits. Restart it for another exchange. Requires Python 3.9+; no external packages.

The browser page at [`labs/tcp-socket/index.html`](labs/tcp-socket/index.html) is an **interactive visualization**, not an actual TCP client. The Python files above open real operating-system TCP sockets.

**First-click insight:** Successful delivery of TCP bytes is not proof that the receiving *application* parsed or accepted the message. The JSON `status_ack` is application-level confirmation, distinct from a TCP ACK.

## Evidence and design

- [Socket lab guide](labs/tcp-socket/README.md)
- [Architecture](docs/architecture.md)
- [Evidence register](docs/evidence.md)
- [Sample local exchange output](labs/tcp-socket/demo-output.txt)
- [Failure experiment backlog](docs/failure-experiments.md)

## Planned — not yet implemented

- UDP client and server comparison
- Linux client, router/firewall, and server virtual machines
- DNS testing and Wireshark/tcpdump packet captures
- TLS handshake and certificate inspection
- Fault injection for DNS, routing, destination ports, and unavailable servers

These are **design targets**, not completed outcomes. Test reports will be added only when experiments are executed.

## Safety and provenance

All robot identifiers and scenarios are fictitious. No real industrial networks, production systems, customer/vendor data, internal designs, credentials, or real robot telemetry are present.

## License

MIT, see [LICENSE](LICENSE).
