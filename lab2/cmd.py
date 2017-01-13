#/usr/bin/
import sys
import pexpect
import re
import os
#import device
import routercli
import time


def CFG(ip,username,password,prompt):
  syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
  try:
    login=pexpect.spawn (syntax)
    login.expect("[P|p]assword:", timeout=180)
    login.sendline(password)
    login.expect("#",timeout=60)
    #print login.before
    login.sendline('terminal len 0')
    login.expect('#',timeout=60)
    print "1.======",login.before
    return login
  except Exception as e:
    print "Problem while setting boot string",name,e
    print login.before
    return "ERROR"



if len(sys.argv) !=3:
  print "Usage !! python2 cmd.py device_ipaddress cli_filename"
  sys.exit()

mgmt_ip=sys.argv[1]
print mgmt_ip
#sys.exit()
password='insieme'
password2='Cisco12345'
filename=sys.argv[2]
file=open(filename,'r')
data=file.read()
print data
clis=re.split('\n',data)
count=1

login=CFG(mgmt_ip,'admin',password,'#')
for cli in clis:
 login.sendline(cli)
 time.sleep(1)
 login.expect('#',timeout=30)
 print login.before
login.close()


