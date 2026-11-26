"""Real HTTP integration: client -> inspecting proxy -> local Python origin."""

import http.client
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

PROXY = Path(__file__).resolve().parents[1] / "proxy.py"


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_port(port):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError(f"Port {port} did not open")


class ProxyIntegrationTest(unittest.TestCase):
    def test_get_and_conditional_get(self):
        with tempfile.TemporaryDirectory() as tempdir:
            doc = Path(tempdir) / "sample.txt"
            doc.write_text("Synthetic network evidence\n", encoding="utf-8")
            origin_port = free_port()
            proxy_port = free_port()
            origin = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(origin_port),
                 "--bind", "127.0.0.1", "--directory", tempdir],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            proxy = None
            try:
                wait_for_port(origin_port)
                proxy = subprocess.Popen(
                    [sys.executable, str(PROXY), "--port", str(proxy_port),
                     "--upstream-port", str(origin_port)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                wait_for_port(proxy_port)
                connection = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=3)
                connection.request("GET", "/sample.txt")
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                modified = response.getheader("Last-Modified")
                self.assertTrue(modified)
                self.assertEqual(response.read(), b"Synthetic network evidence\n")
                connection.close()

                connection = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=3)
                connection.request("GET", "/sample.txt", headers={"If-Modified-Since": modified})
                response = connection.getresponse()
                self.assertEqual(response.status, 304)
                self.assertEqual(response.read(), b"")
                connection.close()
            finally:
                if proxy:
                    proxy.terminate()
                    proxy.wait(timeout=5)
                origin.terminate()
                origin.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
