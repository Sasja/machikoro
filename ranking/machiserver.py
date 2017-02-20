#!/usr/bin/env python
import os
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import pprint

import ranking

def debug(message):
    print message
    pass

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        rank = ranking.Ranking("ranky.rnk")
        self.wfile.write(pprint.pformat(rank.getRanking()))

    def do_POST(self):
        self._set_headers()
        length = int(self.headers.getheader('content-length'))
        requestString = self.rfile.read(length)
        requestDict = json.loads(requestString)
        self.wfile.write(requestDict)

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
    httpd = HTTPServer(address, Handler)

    httpd.serve_forever()
