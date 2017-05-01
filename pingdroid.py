#!/usr/bin/python
# Every x seconds pings a series of hosts to see if they are online.

import os
import datetime

filename = "/home/ctrler/bin/detectdroid/machines.config"


with open(filename) as f_in:
  lines = (line.rstrip() for line in f_in) # All lines including the blank ones
  lines = (line for line in lines if line) # Non-blank lines
  for line in lines:
    timestmp =  datetime.datetime.now()
    hostname = line.split(' ')[0]
    owner = line.split(' ')[1]
    response = os.system('ping -c5 -w10 -t255 ' + hostname + ' > /dev/null 2>&1')
    if response == 0:
      print owner, 'present at', timestmp
