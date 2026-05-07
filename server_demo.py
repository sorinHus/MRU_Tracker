#!/usr/bin/env python3
"""
HR Records Manager - Demo Server
=================================
Usage:  python server_demo.py
Access: http://localhost:8080
"""
import json, os, socket, threading, time, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT      = 8080
BASE      = Path(__file__).parent
PROG_FILE = BASE / 'progress.json'
HTML_FILE = BASE / 'hr_dosare_manager_DEMO.html'

CORS = [
    ('Access-Control-Allow-Origin',  '*'),
    ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
    ('Access-Control-Allow-Headers', 'Content-Type, Accept'),
    ('Cache-Control',                'no-cache, no-store'),
]

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in CORS: self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        print(f'  GET  {self.path}  [{self.client_address[0]}]')
        if self.path in ('/', '/index.html', ''):
            self._file(HTML_FILE, 'text/html; charset=utf-8')
        elif self.path.startswith('/progress.json') or self.path.startswith('/progres.json'):
            if PROG_FILE.exists():
                self._file(PROG_FILE, 'application/json; charset=utf-8')
            else:
                self._json({'done': [], 'ops': {}, 'savedAt': None})
        else:
            self._404()

    def do_POST(self):
        if self.path.startswith('/progress.json') or self.path.startswith('/progres.json'):
            n = int(self.headers.get('Content-Length', 0))
            try:
                data = json.loads(self.rfile.read(n))
                PROG_FILE.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2),
                    encoding='utf-8')
                cnt = len(data.get('done', []))
                print(f'  POST saved: {cnt} records completed')
                self._json({'ok': True, 'count': cnt})
            except Exception as e:
                print(f'  POST error: {e}')
                self._json({'ok': False, 'error': str(e)})
        else:
            self._404()

    def _file(self, path, ctype):
        try:
            body = Path(path).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            for k, v in CORS: self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self._404()

    def _json(self, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        for k, v in CORS: self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _404(self):
        self.send_response(404)
        for k, v in CORS: self.send_header(k, v)
        self.end_headers()

    def log_message(self, *a): pass  # using print instead


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'


def create_shortcut(ip):
    bat = BASE / 'OPEN_APP.bat'
    bat.write_text(
        f'@echo off\nstart "" "http://{ip}:{PORT}"\n',
        encoding='utf-8')
    print(f'  Created: OPEN_APP.bat  →  http://{ip}:{PORT}')


os.chdir(BASE)
ip      = get_ip()
net_url = f'http://{ip}:{PORT}'
loc_url = f'http://localhost:{PORT}'

if not HTML_FILE.exists():
    print(f'\n  ERROR: {HTML_FILE.name} not found in this folder!')
    print(f'  Place server_demo.py and {HTML_FILE.name} in the same folder.\n')
    input('Press Enter to close...')
    raise SystemExit(1)

create_shortcut(ip)

print()
print('╔══════════════════════════════════════════════════════╗')
print('║         HR Records Manager – Server RUNNING          ║')
print('╠══════════════════════════════════════════════════════╣')
print(f'║  Local  :  {loc_url:<43s}║')
print(f'║  Network:  {net_url:<43s}║')
print(f'║                                                      ║')
print(f'║  Share OPEN_APP.bat with other users on the network  ║')
print(f'║  Stop server: Ctrl+C or close this window            ║')
print('╚══════════════════════════════════════════════════════╝')
print()
print('  Waiting for connections...')
print()

threading.Thread(
    target=lambda: (time.sleep(1.5), webbrowser.open(loc_url)),
    daemon=True).start()

try:
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
except KeyboardInterrupt:
    print('\n  Server stopped.')
except OSError as e:
    if 'Address already in use' in str(e):
        print(f'\n  ERROR: Port {PORT} is already in use.')
        print(f'  Close other instances or restart your PC.')
    else:
        print(f'\n  ERROR: {e}')
    input('\nPress Enter to close...')
