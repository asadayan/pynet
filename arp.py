#/usr/bin/
import pexpect
import re
import device
import time


def CFG(ip,username,password,prompt):
  syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
  try:
    login=pexpect.spawn (syntax)
    login.expect("[P|p]assword:", timeout=180)
    login.sendline(password)
    login.expect("#",timeout=60)
    print login.before
    login.sendline('terminal len 0')
    login.expect('#',timeout=60)
    print "1.======",login.before
    login.sendline('show ip arp | i CP | count')
    time.sleep(2)
    login.expect('#',timeout=60)
    data=login.before
    print "2.=======",login.before
    out=re.findall(r'\d+',data)
    print out
    login.close()
    return int(out[0])
  except Exception as e:
    print "Problem while getting arp details",prompt,e
    print login.before
    return "ERROR"

