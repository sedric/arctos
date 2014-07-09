#!/usr/bin/env python

import daemon
import os
from arctos import main as httpd

with daemon.DaemonContext(working_directory=os.getcwd()):
  httpd()
