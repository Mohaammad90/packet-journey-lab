# Architecture — evolving independent lab

## Phase 1: verified TCP socket interaction

```text
Synthetic robot client (Python)                  Fictional fleet service (Python)
127.0.0.1:ephemeral_port                        127.0.0.1:12000
    |                                                    |
    +------------------- TCP connect ------------------->|
    +---------- robot_status JSON, newline ------------>|
    |<--------- status_ack JSON, newline ----------------+
```

The server binds and listens; its `accept()` returns a connected socket. The client connects, sends an application-layer JSON record, and waits for a distinct application-level `status_ack`. TCP acknowledgments do not themselves attest that the server parsed or accepted the JSON.

## Phase 2: planned routed virtual lab

```text
Linux client VM  ----  Linux router / firewall VM  ----  Linux server VM
   DNS client                controlled routes              services
   TCP/UDP client           filtering and failures         TCP/UDP endpoints
```

This second diagram is a **design target**, not a deployment record. Its configuration and verification will be added only once built and tested.

## Scope and evidence standard

Every claim of successful behavior must link to reproducible source, the test command, actual logs/captures, and results. Packet captures and performance metrics are not asserted until measured.
