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
    if channel in alloc and "data" in alloc[channel]:
      return True
    else:
      return False

  def send_data_to_client(self, channel):
    try:
      if not alloc[channel]["data"]:
        raise KeyError('No data in channel')
    except KeyError:
      raise KeyError('No channel')
    self.send_response(200)
    self.send_header('Content-Length ', len(alloc[channel]["data"]))
    self.send_header('Connection', 'close')
    self.end_headers()
    self.wfile.write(alloc[channel]["data"])

  def send_error_to_client(self):
    self.send_response(404)
    self.send_header('Connection', 'close')
    self.end_headers()
    self.wfile.write('')

  def do_GET(self):
    args = self.path[1::].split('?',1)
    channel = args[0]
    ts = time.time()
    if len(args) == 2:
      args = args[1].split('&')

    # Normal operations
    if not "last" in args:
      while not self.data_present_in_channel(channel):
        time.sleep(1/2)
      while True:
        try:
          if ts < alloc[channel]["ts"]:
            self.send_data_to_client(channel)
            break
        except KeyError:
          # Strange bug, happen when sleep <= 1/2
          # Might be because it try to read the value when a POST rewrite it
          pass
        time.sleep(1)
      time.sleep(1/2)

    # For thoses who want an answer NOW.
    if "last" in args:
      try:
        self.send_data_to_client(channel)
      except KeyError:
        self.send_error_to_client()


  def do_POST(self):
    args = self.path[1::].split('?',1)
    channel = args[0]
    alloc[channel] = {}
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
    alloc[channel]["ts"] = time.time()
    alloc[channel]["data"] = postvars

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
