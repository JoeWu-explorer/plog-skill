"""THROWAWAY: run with python3 prototypes/look-system/serve.py."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

if __name__ == '__main__':
    os.chdir(Path(__file__).resolve().parents[2])
    print('http://127.0.0.1:4174/prototypes/look-system/?variant=A', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 4174), SimpleHTTPRequestHandler).serve_forever()
