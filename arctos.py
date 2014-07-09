#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import cgi
import string
#import time

alloc = {}

class Request_Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  global alloc

  def get_content(self):
    index = self.path.translate(string.maketrans("/","z"))
    self.wfile.write(alloc[index])

  def do_GET(self):
# Should work, but it seems that we need to have a threaded python program
#    while True:
#      try:
#        self.get_content()
#      except KeyError:
#        time.sleep(1)
#
# So let's continue with this for now
    try:
      self.get_content()
    except KeyError:
      self.send_response(404)
      self.end_headers()

  def do_POST(self):
    index = self.path.translate(string.maketrans("/","z"))
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
      postvars = cgi.parse_multipart(self.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
      length = int(self.headers.getheader('content-length'))
      postvars = self.rfile.read(length)
    else:
      postvars = {}
    self.send_response(200)
    self.end_headers()
    alloc[index] = postvars

def main():
  port = 8080
  server = BaseHTTPServer.HTTPServer(('', port), Request_Handler)
  server.serve_forever()

if __name__ == "__main__":
    main()
