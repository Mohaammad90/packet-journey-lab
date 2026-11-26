# Failure experiments and backlog

Experiments will be documented with: hypothesis, reproducible steps, observed symptom, logs/packet captures, root cause, and fix.

| ID | Planned fault | Expected observable | Status |
| --- | --- | --- | --- |
| F-01 | Stop TCP server before client connect | Connection failure/refusal depending on OS/network | Not run |
| F-02 | Connect TCP client to incorrect port | Connection failure/refusal depending on listener and firewall | Not run |
| F-03 | Configure invalid DNS resolution | Name lookup fails before TCP connection | Not run |
| F-04 | Remove a route between Linux VMs | No route / timeout depending on topology | Not run |
| F-05 | Firewall blocks destination port | Drop or rejection depending on policy | Not run |
| F-06 | Simulate loss/latency | Measure transfer and retry behavior | Not run |
| F-07 | Stop localhost HTTP origin while inspection proxy stays running | Proxy returns HTTP 502; after origin restart, HTTP 200 | **Completed 2026-11-26** — [evidence](http-proxy-failure-recovery.md) |
