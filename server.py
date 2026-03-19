#!/usr/bin/env python3
import http.server, base64, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))
            for item in body:
                fname = item['filename']
                data = item['data']
                # strip data URL prefix
                data = re.sub(r'^data:[^;]+;base64,', '', data)
                path = os.path.join(ROOT, fname)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb') as f:
                    f.write(base64.b64decode(data))
                print(f"Saved: {path}")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, fmt, *args):
        import sys; print(fmt % args, file=sys.stderr)

if __name__ == '__main__':
    os.chdir(ROOT)
    server = http.server.HTTPServer(('', 8766), Handler)
    print("Server running on :8766")
    server.serve_forever()
