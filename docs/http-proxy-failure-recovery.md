# HTTP-FAIL-001 — Origin outage and recovery through a localhost HTTP proxy

## Scope

**Date:** 26 November 2026 (UTC)  
**Environment:** macOS, Python's `http.server` as origin on `127.0.0.1:8000`, fixed-origin inspection reverse proxy on `127.0.0.1:8080`, and `curl` as the client.

**Purpose:** Distinguish failures at the client's TCP connection to the proxy from failures of the proxy's upstream TCP connection to the origin. Observe recovery when the upstream comes back online.

These observations were supplied from an interactive local terminal session by the experiment operator. The commands and response excerpts below are an **evidence transcription**, not new automated assertions or an independently archived packet capture.

## Procedure and observed results

1. **Healthy baseline:** With both processes running, requesting `http://127.0.0.1:8080/README.md` returned HTTP **200 OK**. Proxy logs included `PROXY received: GET /README.md` and `PROXY forwarded response: 200 OK`.
2. **Proxy unavailable (control case):** An attempt while nothing was listening on port 8080 failed at the TCP connection stage:
   ```text
   curl: (7) Failed to connect to 127.0.0.1 port 8080
   ```
   No HTTP response was received.
3. **Origin outage:** The proxy was restarted on port 8080 but the origin on port 8000 was intentionally left stopped. The client requested the same URL and observed:
   ```http
   HTTP/1.1 502 Upstream server unavailable
   Content-Type: text/html;charset=utf-8
   Content-Length: 362
   ```
   Reported response timestamp: `Thu, 26 Nov 2026 23:03:36 GMT`. The proxy's implementation generates this response after its connection to the origin fails.
4. **Recovery:** The origin was restarted on port 8000; the proxy remained running. Repeating the same request returned:
   ```http
   HTTP/1.1 200 OK
   Content-type: text/markdown
   Content-Length: 3380
   ```
   Reported response timestamp: `Thu, 26 Nov 2026 23:05:19 GMT`. The response body began with `# Packet Journey Lab`, confirming the requested file was served.

## Diagnosis

- `curl: (7)` indicates the **client failed to establish a TCP connection to the proxy** and received no HTTP response.
- `HTTP 502` indicates the **client successfully reached the proxy**, but the proxy could not reach its configured origin; the proxy generated an HTTP error.
- `HTTP 200` after restarting the origin confirms that this upstream dependency was restored for the tested request, without needing to restart or reconfigure the proxy.

## Reproduce locally

From the repository root, in separate terminals:

```bash
# Terminal A: origin
python3 -m http.server 8000 --bind 127.0.0.1

# Terminal B: proxy
python3 labs/http-proxy/proxy.py

# Terminal C: client
curl -i http://127.0.0.1:8080/README.md
```

Press Ctrl+C in Terminal A to stop the origin and repeat the request in Terminal C (expect HTTP 502). Restart Terminal A and repeat again (expect HTTP 200).

## Limits

A single, local, manually triggered outage/recovery test; no automatic retries, load balancer, real distributed hosts, packet captures, or production availability conclusions. Port numbers, timestamps, and response body size are specific to this experiment.
