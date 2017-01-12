#/usr/bin/
import pexpect
import re
import device
import os
import sys
import time

if len(sys.argv) !=2:
  print "Usage !! python2 mac_acl.py <asw|psw|dsw> > "
  sys.exit()

input=sys.argv[1]

asw_consoles=[]
for i in range(1,9):
  for j in range(1,3):
    function='device.IPCONSASW'+str(i)+str(j)
    asw_consoles.append((eval(function+'()')))

asw_ssh=[]
for i in range(1,9):
  for j in range(1,3):
    function='device.IPSSHASW'+str(i)+str(j)
    asw_ssh.append((eval(function+'()')))

dsw_consoles=[]
for i in range(1,9):
  function='device.IPCONSDSW'+str(i)
  dsw_consoles.append((eval(function+'()')))

dsw_ssh=[]
for i in range(1,9):
  function='device.IPSSHDSW'+str(i)
  dsw_ssh.append((eval(function+'()')))

psw_consoles=[]
for i in range(1,5):
  function='device.IPCONSPSW'+str(i)
  psw_consoles.append((eval(function+'()')))

psw_ssh=[]
for i in range(1,5):
  function='device.IPSSHPSW'+str(i)
  psw_ssh.append((eval(function+'()')))

if input=='psw': dev=psw_ssh
elif input=='dsw': dev=dsw_ssh
elif input=='asw': dev=asw_ssh

if input[0]=='a' and len(input) != len('asw'):
  for i in asw_ssh:
    #print i
    if i[1]==input:
      device=i[1]
      dev_addr=i[0]
elif input[0]=='d' and len(input) != len('dsw'):
  for i in dsw_ssh:
    if i[1]==input:
      device=i[1]
      dev_addr=i[0]
elif input[0]=='p' and len(input) != len('psw'):
  for i in psw_ssh:
    if i[1]==input:
      device=i[1]
      dev_addr=i[0]
username='admin'
password='nbv12345'
cli1='mac access-list arp-eth-1-'
cli2='statistics per-entry'
cli3='10 permit any ffff.ffff.ffff 0000.0000.0000 0x806'
cli4='20 permit any any'
cli5='interface port-channel'
cli6='mac port access-group arp-eth-1-'
try:
  dev
  devx=1
  devicex=0
  print "SSH info:",dev
except:
  try:
    device
    dev_addr
    devicex=1
    devx=0
    print "SSH info:",device,dev_addr
  except:
    print "Error in defining Variables"
if devx==1:
  for ip,name in dev:
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
      login.sendline('config t')
      time.sleep(1)
      login.expect('#',timeout=30)
      login.before
    except Exception as e:
      print "Problem while getting arp details",prompt,e
      print login.before
    count=1

    for i in range(101,149):
      cli01=cli1+str(count)
      clipo=cli5+str(i)
      climac=cli6+str(count)
      login.sendline(cli01)
      #time.sleep(1)
      login.expect('#',timeout=30)
      login.sendline(cli2)
      #time.sleep(1)
      login.expect('#',timeout=30)
      login.sendline(cli3)
      #time.sleep(1)
      login.expect('#',timeout=30)
      login.sendline(cli4)
      #time.sleep(1)
      login.expect('#',timeout=30)
      login.sendline(clipo)
      #time.sleep(1)
      login.expect('#',timeout=30)
      login.sendline(climac)
      #time.sleep(1)
      login.expect('#',timeout=30)
      count +=1
      print login.before
  login.close()
elif devicex==1:
  ip=dev_addr
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
    login.sendline('config t')
    time.sleep(1)
    login.expect('#',timeout=30)
    login.before
  except Exception as e:
    print "Problem while getting arp details",prompt,e
    print login.before
  count=1
  for i in range(101,149):
    cli01=cli1+str(count)
    clipo=cli5+str(i)
    climac=cli6+str(count)
    login.sendline(cli01)
    #time.sleep(1)
    login.expect('#',timeout=30)
    login.sendline(cli2)
    #time.sleep(1)
    login.expect('#',timeout=30)
    login.sendline(cli3)
    #time.sleep(1)
    login.expect('#',timeout=30)
    login.sendline(cli4)
    #time.sleep(1)
    login.expect('#',timeout=30)
    login.sendline(clipo)
    #time.sleep(1)
    login.expect('#',timeout=30)
    login.sendline(climac)
    #time.sleep(1)
    login.expect('#',timeout=30)
    count +=1
    print login.before
  login.close()

