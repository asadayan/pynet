#/usr/bin/
import sys
import pexpect
import os
import re

if len(sys.argv) != 3:
  print "usage python program_name <First IP address> <Last IP address>  "
  sys.exit()
#import pdb; pdb.set_trace()
ip_first=sys.argv[1]
ip_last=sys.argv[2]
net=re.split('\.',ip_first)
net_last=re.split('\.',ip_last)
ipnet=str(net[0])+"."+str(net[1])+"."+str(net[2])+"."
range_first=int(net[3])
range_last=int(net_last[3])
range_last=range_last+1
#start_ip=sys.argv[5]
dict={}
dicth={}
print '\n','+'*120
print '\t'*1,'OSC REBOOT'
print '+'*120,'\n'
#ip_oct=re.split('\.',start_ip)
#ip1=int(ip_oct[3])
#ip2=int(ip_oct[2])
#ip3=int(ip_oct[1])
#ip4=int(ip_oct[0])


for each in range(int(range_first),int(range_last)):
    ip=ipnet+str(each)
    child = pexpect.spawn ('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null sysadmin@%s'%ip)
    child.expect("[P|p]assword:",timeout=180)
    child.sendline("C1sc0123")
    child.expect("$",timeout=90)
    name=child.before
    child.sendline("sudo su")
    child.expect("#",timeout=60)
    print child.before
    cli1= "netstat -nr"
    cli2="ifconfig "
    cli3="reboot"
    child.sendline(cli1)
    child.expect("#",timeout=60)
    #print child.before
    child.sendline(cli2)
    child.expect("#",timeout=60)
    int_ip= child.before
    int_ip_out=re.findall(r"inet addr:[\d]+\.[\d]+\.[\d]+\.[\d]+",int_ip)
    print "OSC IP ADDRESS:", int_ip_out
    child.sendline(cli3)
    child.expect("#",timeout=60)
    print child.before
    print "\t"*1,'finished configuring ',ipnet+str(each)

