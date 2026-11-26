# Evidence register

## TCP-001 — real localhost TCP message exchange

**Implementation:** `labs/tcp-socket/server.py` and `labs/tcp-socket/client.py`.

**Procedure:** `python3 -m unittest discover -s labs/tcp-socket/tests -v` at repository root.

**Expected behavior:** The test launches a TCP server on loopback with an OS-selected port, starts the client as a separate process, and checks that the server receives a synthetic `robot_status` and returns `status_ack` with `accepted: true`.

**Archived output:** [`labs/tcp-socket/demo-output.txt`](../labs/tcp-socket/demo-output.txt). The archived output was generated from an earlier local run and is preserved as supporting example output; re-run the automated test for current execution evidence.

**Limitations:** This tests loopback only; it makes no claims about routed networking, TLS, real robots, packet captures or loss behavior.

## HTTP-FAIL-001 — localhost origin failure and recovery

**Recorded interactive terminal observations:** [Read the failure → diagnosis → recovery report](http-proxy-failure-recovery.md).

**Observed:** A stopped proxy produced `curl: (7)`; a running proxy with a stopped origin produced HTTP `502`; restoring the origin produced HTTP `200` and the file body. This is a local manually reproduced experiment, not an automatically monitored production outage.
