# /usr/bin/
import sys
import httplib
import urllib
import json
import re

if len(sys.argv) != 2:
    print "usage python program_name <subnet to match example 112.1. or 111.1.2.>"
    sys.exit()
subnet=sys.argv[1]


url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
data={}
d1={}
d2={}
false=[]
true=[]
id=[]
ip_list=[]
id_list=[]
net_list=[]
id_ip={}
false_list=[]
true_list=[]
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/host")
r1=conn.getresponse()
data=r1.read()
#out=re.findall(r"\"id\":\"[\d\w-]+\"",data)
id_list=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
ip_list=re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+",data)
id_ip=dict(zip(ip_list,id_list))
#print id_ip
for i in ip_list:
  ipmatch=re.split('\.',i)
  ip_network=ipmatch[0]+"."+ipmatch[1]+"."
  if (re.search(subnet,ip_network)):
    net_list.append(i)
#print net_list
conn.close
conn = httplib.HTTPConnection(url, 8181)
for i in net_list:
  url="/vnet/cache/host?id="+id_ip[i]
  conn.request("GET", url)
  data=conn.getresponse()
  out=data.read()
  #print out
  arp_no=  re.findall(r"false",out)
  if arp_no:
    false.append(arp_no)
    false_list.append(out)
  arp= re.findall(r"true",out)
  if arp:
    true.append(arp)
    true_list.append(out)
#print "no_arp:",false
#print "arp:",true

print "Unlearned ARP host count:",len(false)
print "Learned ARP host count:",len(true)
print " Total host count:",len(net_list)
if false_list:
  print "Unlearned ARP List sample:",false_list[0]
if true_list:
  print "Learned ARP list sample:",true_list[0]
conn.close()



