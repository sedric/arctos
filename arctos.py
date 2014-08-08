#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer, cgi
from SocketServer import ThreadingMixIn
import string
import time

# hashtable containing open channels and datas
alloc = {}

class Request_Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  global alloc
  protocol_version = 'HTTP/1.1'

  def data_present_in_channel(self,channel):
    if channel in alloc:
      return True
    else:
      return False

  def do_GET(self):
    channel = self.path.translate(string.maketrans("/","z"))
    while not self.data_present_in_channel(channel):
      time.sleep(1)
    self.send_response(200)
    self.send_header('Content-Length ', len(alloc[channel]))
    self.send_header('Connection', 'close')
    self.end_headers()
    self.wfile.write(alloc[channel])

  def do_POST(self):
    channel = self.path.translate(string.maketrans("/","z"))
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
      postvars = cgi.parse_multipart(self.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
      length = int(self.headers.getheader('content-length'))
      postvars = self.rfile.read(length)
    else:
      postvars = {}
    self.send_response(200)
    self.send_header('Connection', 'close')
    self.end_headers()
    alloc[channel] = postvars

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
      """Handle requests in a separate thread."""

def httpd(i, p):
  server = ThreadedHTTPServer((i, p), Request_Handler)
  server.serve_forever()

def main():
  import argparse

  parser = argparse.ArgumentParser(description='Messaging HTTP server')
  parser.add_argument('-i', action='store',
                      default="0.0.0.0",
                      help='Interface used (default : all)')
  parser.add_argument('-p', action='store',
                      type=int, default='8080',
                      help='Port used for listen (default : 8080)')
  args = parser.parse_args()
  args = dict(args._get_kwargs())

  httpd(args['i'], args['p'])

if __name__ == "__main__":
    main()
