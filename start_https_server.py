#!/usr/bin/env python3
from http import server as BaseHTTPServer
import ssl

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    # When an HTTP POST request is received
    def do_POST(self):
        # Print the body of the request
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print('POST data: ', body)
        self.send_response(200)
        self.end_headers()

# Enable HTTPS server on port 443 (all interfaces) using the specified full certificate chain and private key files
httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', 443), Handler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='fullchain.pem', server_side=True, keyfile="key.pem")
httpd.serve_forever()
