#!/usr/bin/env python3
from http import server
import ssl
class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);

httpd = server.HTTPServer(('0.0.0.0', 443), Handler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='cert.pem', server_side=True, keyfile="key.pem")
httpd.serve_forever()          
