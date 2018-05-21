#!/usr/bin/python

import papi
import sys
import getpass
import json
import time
import os
import getopt

def touch_perm (file_name):
  path = "/namespace/" + file_name + "?acl"
  (status, reason, resp) = papi.call ('localhost', '8080', 'GET', path,  '', 'any', 'text/plain', 'root', password)
  if status != 200:
    error_str = "ERROR: Bad Status: " + `status`
    sys.stderr.write (err_str)
    exit (status)
  metadata = json.loads (resp)
  if metadata['authoritative'] != 'acl':
    return
  if status != 200:
    error_str = "ERROR: Bad Status[2]: " + `status`
    sys.stderr.write (err_str)
    exit (status)
  (status, reason, resp2) = papi.call ('localhost', 8080, 'PUT', path, resp, 'any', 'application/json', 'root', password)
  if status != 200:
    error_str = "ERROR: Bad Status[3]: " + `status`
    sys.stderr.write (err_str)
    exit (status)
  (status, reason, resp) = papi.call ('localhost', '8080', 'GET', path,  '', 'any', 'text/plain', 'root', password)
  if status != 200:
    err_str = "ERROR: Bad Status[4]: " + `status`
    sys.stderr.write (err_str)
    exit (status)
  (status, reason, resp3) = papi.call ('localhost', 8080, 'PUT', path, resp, 'any', 'application/json', 'root', password)
  if status != 200:
    err_str = "ERROR: Bad Status[5]: " + `status`
    sys.stderr.write (err_str)
    exit (status)
  return

global password
global debug
optlist, args = getopt.getopt(sys.argv[1:],'D')
debug = False
for o, a in optlist:
  if o == '-D':
    debug = True
password = getpass.getpass ("Root Password: ")
for dirname, subdirList, filelist in os.walk(args[0]):
  if (debug):
    print ("DEB: DIR: dir: %s" % dirname)
  touch_perm (dirname)
  for fname in filelist:
    file = dirname + "/" + fname
    if (debug):
      print ("\tDEB: FILE: %s" % file)
    touch_perm (file)
    

