#/usr/bin/
import pexpect
import re
import device
import time
import os

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
    #print "1.======",login.before
    login.sendline('show ip arp | i CP | count ; show clock')
    time.sleep(1)
    login.expect('#',timeout=60)
    data=login.before
    print "1.=======",login.before
    out=re.findall(r'\d+',data)
    print out
    return out,login
  except Exception as e:
    print "Problem while getting arp details",prompt,e
    print login.before
    return "ERROR"




ip,prompt=device.IPSSHDSW8()
username='admin'
password='nbv12345'
file=open('arpdelrate-dsw8.txt','w')
output,handler=CFG(ip,username,password,prompt)
arp=int(output[0])
hrs=int(output[1])
mts=int(output[2])
sec=int(output[3])
times=str(hrs)+':'+str(mts)+':'+str(sec)
#print arp
file.write('No of arps:')
file.write(str(arp))
file.write('\n')
file.write('Time:')
file.write(times)
file.write('\n')
oarp=arp
ohrs=hrs
omts=mts
osec=sec
while arp>1:
  handler.sendline('show ip arp | i CP | count ; show clock')
  handler.expect('#',timeout=60)
  data=handler.before
  output=re.findall(r'\d+',data)
  arp=int(output[0])
  hrs=int(output[1])
  mts=int(output[2])
  sec=int(output[3])
  arpc=arp-oarp
  hrsc=hrs-ohrs
  mtsc=mts-omts
  secc=sec-osec
  times=str(hrs)+':'+str(mts)+':'+str(sec)
  timec=str(hrsc)+':'+str(mtsc)+':'+str(secc)
  file.write('Change in ARP:')
  file.write(str(arpc))
  file.write(' for change in time: ')
  file.write(timec)
  file.write('\n')
  file.write('No of arps:')
  file.write(str(arp))
  file.write('\n')
  file.write('Time:')
  file.write(times)
  file.write('\n')
  oarp=arp
  ohrs=hrs
  omts=mts
  osec=sec
  print time,timec
  time.sleep(10)
  print arp,arpc

file.close()
handler.close()
