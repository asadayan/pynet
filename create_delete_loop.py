#/usr/bin/
import sys
import re
import os
import time
import arp
import device

cmd1='python2 job_create_host.py'
cmd2='python2 delete_host_all.py'

for i in range(1,25):
  os.system(cmd1)
  time.sleep(3)
  print "Execute create and delete:",i
  ip,dev=device.IPSSHDSW1()
  arp=CFG(ip,'admin','nbv12345',dev)
  print "Total arp :",arp
  if arp>=210000:
    os.system(cmd2)
  time.sleep(300)
  while arp>5:
    time.sleep(60)
    arp=CFG(ip,'admin','nbv12345',dev)
  time.sleep(5)



