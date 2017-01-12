#/usr/bin/
import pexpect
import re
import time

def SSH(ip,username,password):
  syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
  try:
    login=pexpect.spawn (syntax)
    login.expect("[P|p]assword:", timeout=180)
    login.sendline(password)
    time.sleep(1)
    login.expect("#|$",timeout=60)
    login.sendline('terminal len 0')
    time.sleep(1)
    login.expect('#|$')
    print login.before
    print "ssh module success:"
    return login


  except:
    print "Problem using ssh to",ip
    print login.before
    return "ERROR"

