# /usr/bin/
import sys
import httplib
import urllib
import json
import re
import get_subnet
import time

subnets=get_subnet.subnet()
print "subnets:",subnets



url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
#print "regular expression:",ipaddress
data={}
id=[]
z={}
net_list=[]
idnet=[]
count=0
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/host")
r1=conn.getresponse()
data=r1.read()
id=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
ip=re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+",data)
conn.close()
z=dict(zip(ip,id))
if not id:
  print "No Hosts Created"
  sys.exit()
for subnet in subnets:
  subnet1=re.split('\.',subnet)
  #print z
  print "subnet-split:",subnet1
  for i in ip:
    i1=re.split('\.',i)
    if int(subnet1[3])==0 and int(subnet1[2])==0:
      if subnet1[0]==i1[0] and subnet1[1]==i1[1]:
        net_list.append(i)
    elif subnet1[2]==i1[2] and subnet1[0]==i1[0] and subnet1[1]==i1[1]:
      net_list.append(i)

  #print "Net List:",net_list

  for j in net_list:
     idnet.append(z[j])
  #print idnet

  body={
         "ids":idnet
        }
  #print idnet
  if idnet:
    conn = httplib.HTTPConnection(url, 8181)
    conn.request("POST", "/vnet/host/batchdelete", json.dumps(body), headers)
    resp=conn.getresponse()
    if resp is not None:
      print resp.status, resp.reason
      data = resp.read()
      #print data
      #print resp.status,resp.read()
    print "Number of HOSTS deleted:",len(idnet)
    conn.close()
  idnet=[]
  net_list=[]
  time.sleep(13)



