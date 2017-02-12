#!/usr/bin/env python
import json
import random
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def debug(message):
    print message
    pass

class MachiBotHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        length = int(self.headers.getheader('content-length'))
        requestString = self.rfile.read(length)
        actionRequest = json.loads(requestString)
        choice = chooseAction(actionRequest)
        self.wfile.write(choice)

# RandomBot:
# this is the absolute baseline AI
def chooseAction(actionRequest):
    debug(actionRequest)
    choice = random.choice(actionRequest["options"])
    debug(choice)
    return choice

if __name__ == "__main__":
    address = ('127.0.0.1', 6666)
    httpd = HTTPServer(address, MachiBotHandler)

    httpd.serve_forever()
    #while True:
    #    httpd.handle_request()
