# HTTP inspection proxy (localhost only)

This **reverse proxy** receives HTTP requests on `127.0.0.1:8080`, logs the method/path and conditional header, and forwards the request to the already-running Python HTTP server on `127.0.0.1:8000`.

## Run on Mac

Keep the origin server running in its existing Terminal window:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

In a second Terminal window (from the repository root):

```bash
python3 labs/http-proxy/proxy.py
```

In a third Terminal tab:

```bash
curl -i http://127.0.0.1:8080/README.md
```

The proxy Terminal will print the incoming HTTP method/path, and the origin will log the forwarded request. Compare the direct server port (`8000`) to the proxy port (`8080`).

To reproduce a conditional request through the proxy, substitute your file's actual `Last-Modified` timestamp:

```bash
curl -i -H "If-Modified-Since: Thu, 26 Nov 2026 22:21:03 GMT" http://127.0.0.1:8080/README.md
```

Expected: **304** if the timestamp is equal to or newer than the current modification time, otherwise **200** and a file body.

## Automated integration

```bash
python3 -m unittest discover -s labs/http-proxy/tests -v
```

The test starts an isolated HTTP origin and proxy on OS-selected localhost ports, verifies **200 OK** with a body, then **304 Not Modified** without a body. It runs without third-party packages.

## Important limitations

This experiment is a **fixed-origin, local HTTP reverse proxy**, not a browser-configured general forward proxy. It handles GET and HEAD only. It intentionally does **not** handle HTTPS, CONNECT, cookies, arbitrary targets, production traffic or robust HTTP header semantics. Do not expose it outside localhost. Real packet captures and the textbook's broader caching-proxy implementation remain separate future exercises.
