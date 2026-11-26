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

## Verified: HTTP conditional requests through a local proxy

A **new localhost HTTP inspection proxy** receives HTTP requests on port `8080`, logs them and forwards them to the Python HTTP server on port `8000`. Automated integration tests verify a **200 OK** with a file body and a conditional **304 Not Modified** response without a body.

**[Run the HTTP proxy lab](labs/http-proxy/README.md)** — `python3 labs/http-proxy/proxy.py`

**Automated test:** `python3 -m unittest discover -s labs/http-proxy/tests -v`

This is a fixed-origin reverse proxy, **not** a full browser-configured caching proxy. The textbook's broader proxy implementation remains unfinished.

**Manual fault injection verified:** The local proxy returned **502** when its origin was stopped, and recovered to **200** when the origin restarted. [Read the outage and recovery evidence](docs/http-proxy-failure-recovery.md).

## Evidence and design

- [Socket lab guide](labs/tcp-socket/README.md)
- [Architecture](docs/architecture.md)
- [Evidence register](docs/evidence.md)
- [Sample local exchange output](labs/tcp-socket/demo-output.txt)
- [Failure experiment backlog](docs/failure-experiments.md)

## Planned — not yet implemented

- Browser-configured caching HTTP proxy / complete textbook P11 task
- UDP client and server comparison
- Linux client, router/firewall, and server virtual machines
- DNS testing and Wireshark/tcpdump packet captures
- TLS handshake and certificate inspection
- Additional fault injection for DNS, routing, destination ports, and unavailable hosts beyond the tested localhost origin outage

These are **design targets**, not completed outcomes. Test reports will be added only when experiments are executed.

## Safety and provenance

All robot identifiers and scenarios are fictitious. No real industrial networks, production systems, customer/vendor data, internal designs, credentials, or real robot telemetry are present.

## License

MIT, see [LICENSE](LICENSE).
