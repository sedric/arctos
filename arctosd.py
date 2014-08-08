#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from arctosd import httpd
import daemon
import os, pwd, grp
import fcntl

# This class is released under MIT and GPL licences,
# See http://code.activestate.com/recipes/577911-context-manager-for-a-daemon-pid-file/
class PidFile(object):
  """Context manager that locks a pid file.  Implemented as class
  not generator because daemon.py is calling .__exit__() with no parameters
  instead of the None, None, None specified by PEP-343."""
  # pylint: disable=R0903

  def __init__(self, path):
    self.path = path
    self.pidfile = None

  def __enter__(self):
    self.pidfile = open(self.path, "a+")
    try:
      fcntl.flock(self.pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
      raise SystemExit("Already running according to " + self.path)
    self.pidfile.seek(0)
    self.pidfile.truncate()
    self.pidfile.write(str(os.getpid()))
    self.pidfile.flush()
    self.pidfile.seek(0)
    return self.pidfile

  def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
    try:
      self.pidfile.close()
    except IOError as err:
      # ok if file was just closed elsewhere
      if err.errno != 9:
        raise
    os.remove(self.path)

parser = argparse.ArgumentParser(description='Messaging HTTP daemon')
parser.add_argument('-p', action='store',
                    type=int, default='8080',
                    help='Port used for listen (default : 8080)')
parser.add_argument('-i', action='store',
                    default="0.0.0.0",
                    help='Interface used (default : all)')
parser.add_argument('--pid', action='store',
                    default="/var/run/arctosd.pid",
                    help='where the pid file should be placed (default : /var/run/arctosd.pid')
parser.add_argument('--user', action='store',
                    default="nobody",
                    help='Change to user when daemonize (default : nobody)')
parser.add_argument('--group', action='store',
                    default="nogroup",
                    help='Change to group when daemonize (default : nogroup)')

args = parser.parse_args()
args = dict(args._get_kwargs())

context = daemon.DaemonContext()
context.pidfile = PidFile(args['pid'])
context.uid = pwd.getpwnam(args['user'])[2]
context.gid = grp.getgrnam(args['group'])[2]

with context:
  httpd(args['i'], args['p'])
