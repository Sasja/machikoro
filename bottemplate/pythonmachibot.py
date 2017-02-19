#!/usr/bin/env python
import os
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
    DEFAULT_IP = "0.0.0.0" 
    DEFAULT_PORT = 1337

    if "MACHI_IP" in os.environ:
        print "setting IP from $MACHI_IP"
        ip = os.environ["MACHI_IP"]
    else:
        print "no $MACHI_IP found, using default IP"
        ip = DEFAULT_IP

    if "MACHI_PORT" in os.environ: 
        print "setting PORT from $MACHI_PORT"
        port = int(os.environ["MACHI_PORT"])
    else:
        print "no $MACHI_PORT found, using default PORT"
        port = DEFAULT_PORT
    address = (ip, port)

    print "binding server to {}".format(str(address))
    httpd = HTTPServer(address, MachiBotHandler)

    httpd.serve_forever()
