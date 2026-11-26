"""Local HTTP inspection proxy: browser/curl -> 127.0.0.1:8080 -> origin :8000.

Fixed-origin localhost lab only. Do not expose this toy proxy to external networks.
"""

import argparse
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class InspectingProxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    upstream_port = 8000

    def do_GET(self):
        self.forward_request()

    def do_HEAD(self):
        self.forward_request()

    def forward_request(self):
        if not self.path.startswith("/") or self.path.startswith("//"):
            self.send_error(400, "Only local absolute paths are supported")
            return

        conditional_date = self.headers.get("If-Modified-Since")
        print(f"PROXY received: {self.command} {self.path}", flush=True)
        if conditional_date:
            print(f"PROXY saw If-Modified-Since: {conditional_date}", flush=True)

        forwarded_headers = {"Host": f"127.0.0.1:{self.upstream_port}"}
        if conditional_date:
            forwarded_headers["If-Modified-Since"] = conditional_date
        if self.headers.get("If-None-Match"):
            forwarded_headers["If-None-Match"] = self.headers["If-None-Match"]

        connection = http.client.HTTPConnection("127.0.0.1", self.upstream_port, timeout=5)
        try:
            connection.request(self.command, self.path, headers=forwarded_headers)
            response = connection.getresponse()
            body = response.read() if self.command == "GET" else b""

            # Use response headers from the origin without duplicating Server/Date.
            self.send_response_only(response.status, response.reason)
            for name, value in response.getheaders():
                if name.lower() not in ("connection", "transfer-encoding", "content-length"):
                    self.send_header(name, value)
            declared_length = response.getheader("Content-Length")
            if self.command == "HEAD" and declared_length is not None:
                self.send_header("Content-Length", declared_length)
            else:
                self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command == "GET" and body:
                self.wfile.write(body)
            self.close_connection = True
            print(f"PROXY forwarded response: {response.status} {response.reason}", flush=True)
        except (OSError, http.client.HTTPException) as exc:
            self.send_error(502, "Upstream server unavailable")
            print(f"PROXY upstream error: {type(exc).__name__}: {exc}", flush=True)
        finally:
            connection.close()


def main():
    parser = argparse.ArgumentParser(description="Local HTTP request-inspection proxy")
    parser.add_argument("--port", type=int, default=8080, help="proxy listening port")
    parser.add_argument("--upstream-port", type=int, default=8000, help="origin HTTP port")
    args = parser.parse_args()
    InspectingProxy.upstream_port = args.upstream_port
    with ThreadingHTTPServer(("127.0.0.1", args.port), InspectingProxy) as server:
        print(f"PROXY listening at http://127.0.0.1:{server.server_port}/", flush=True)
        print(f"PROXY forwarding to http://127.0.0.1:{args.upstream_port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("PROXY shutting down", flush=True)


if __name__ == "__main__":
    main()
