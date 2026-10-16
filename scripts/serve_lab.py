import functools
import http.server
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent / "lab"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(NoCacheHandler, directory=str(LAB))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"Lab running at http://localhost:{port}  (Ctrl+C to stop)")
        server.serve_forever()


if __name__ == "__main__":
    main()
