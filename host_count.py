# /usr/bin/
import sys
import httplib
import urllib
import json
import re
import get_subnet


neti_list=[]
url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
subnets=get_subnet.subnet()
print "subnets:",subnets
for out in subnets:
  ip_input=re.split('\.',out)
  net=ip_input[0]+"."+ip_input[1]+"."
  neti_list.append(net)
data={}
z={}
id=[]
net_list=[]
id_list=[]
unlearn=0
true_list=[]
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/host")
r1=conn.getresponse()
data=r1.read()
#print data
id=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
ip=re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+",data)
z=dict(zip(ip,id))
print "Total hosts in data store:",len(z)
for j in neti_list:
  for i in z.keys():
    ipmatch=re.split('\.',i)
    ip_network=ipmatch[0]+"."+ipmatch[1]+"."
    if (re.search(j,ip_network)):
      net_list.append(i)
      id_list.append(z[i])
  print "Host Count for Network:",j+"0.0:","\t"*3,len(net_list)
  net_list=[]
conn.close()
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/cache/host")
r2=conn.getresponse()
data0=r2.read()
arp_list=re.split("\"id:\"",data0)
#print arp_list
id1=re.findall(r"id...([\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+)",data0)
ip1=re.findall(r"ip...([\d]+\.[\d]+\.[\d]+\.[\d]+)",data0)
vtep=re.findall(r"\"vtep\":\"([\d]+\.[\d]+\.[\d]+\.[\d]+)",data0)
z1=dict(zip(ip1,id1))
z2=dict(zip(ip1,vtep))
print "Total hosts in Cache:",len(z1)
for k in neti_list:
  for m in z1.keys():
    ipmatch0=re.split('\.',m)
    ip_network0=ipmatch0[0]+"."+ipmatch0[1]+"."
    if (re.search(k,ip_network0)):
      net_list.append(m)
      id_list.append(z1[m])
  print "Host Count in Cache for Network:","\t"*1,k+"0.0:","\t"*2,len(net_list)
  net_list=[]
  for o in z2.keys():
    ipmatch1=re.split('\.',o)
    ip_network1=ipmatch1[0]+"."+ipmatch1[1]+"."
    if z2[o]=="255.255.255.255" and (re.search(k,ip_network1)):
      unlearn=unlearn+1
    elif (re.search(k,ip_network1)) and z2[o] != "255.255.255.255":
      true_list.append(z2[o])
  print "UNLEARNED ARP host count:","\t"*2,k+"0.0:","\t"*2,unlearn
  print "LEARNED ARP host count:","\t"*2,k+"0.0:","\t"*2,len(true_list),"\n"
  true_list=[]
  unlearn=0

conn.close()




