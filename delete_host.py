# /usr/bin/
import sys
import httplib
import urllib
import json
import re

if len(sys.argv) != 3:
    print "usage python program_name <subnet to match example 112.1. or 111.1.2.> <No. of hosts to delete>"
    sys.exit()
subnet=sys.argv[1]
num=int(sys.argv[2])
url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
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
z=dict(zip(ip,id))
if not id:
  print "No Hosts Created"
  sys.exit()

for i in ip:
  if (re.search(subnet,i)) and len(net_list)<=num:
    net_list.append(i)

for j in net_list:
   idnet.append(z[j])

conn.close()
body={
       "ids":idnet
      }
#print idnet

for i in ip:
 path="/vnet/host/"+str(z[i])
 conn = httplib.HTTPConnection(url, 8181)
 conn.request("DELETE",path , json.dumps(body), headers)
 resp=conn.getresponse()
 if resp is not None:
   print resp.status, resp.reason
   data = resp.read()
   print data
 conn.close()


print "Number of HOSTS deleted:",len(idnet)



