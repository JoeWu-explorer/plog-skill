"""THROWAWAY PROTOTYPE — serve the layout recipe comparison locally."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PORT = 4173


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    print(f"Layout prototype: http://127.0.0.1:{PORT}/prototypes/layout-recipes/?variant=A")
    ThreadingHTTPServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler).serve_forever()
