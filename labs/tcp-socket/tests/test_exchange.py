"""End-to-end test: starts the TCP server and connects to it over localhost."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SocketExchangeTest(unittest.TestCase):
    def test_real_tcp_exchange(self):
        # Port 0 delegates port selection to the operating system.
        server = subprocess.Popen(
            [sys.executable, "-u", str(ROOT / "server.py"), "--port", "0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            first_line = server.stdout.readline()
            self.assertIn("SERVER listening on 127.0.0.1:", first_line)
            port = int(first_line.rsplit(":", 1)[1])
            client = subprocess.run(
                [sys.executable, str(ROOT / "client.py"), "--port", str(port)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(client.returncode, 0, client.stderr)
            self.assertIn("CLIENT TCP established", client.stdout)
            self.assertIn("'accepted': True", client.stdout)
            server_output, server_error = server.communicate(timeout=10)
            self.assertEqual(server.returncode, 0, server_error)
            self.assertIn("SERVER received application message:", server_output)
            self.assertIn("SERVER sent application response:", server_output)
        finally:
            if server.poll() is None:
                server.kill()
                server.communicate()


if __name__ == "__main__":
    unittest.main()
