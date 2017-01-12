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
id=[]
net_list=[]
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/host")
r1=conn.getresponse()
data=r1.read()
#out=re.findall(r"\"id\":\"[\d\w-]+\"",data)
id=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
ip=re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+",data)
for i in ip:
  if (re.search(subnet,i)):
    net_list.append(i)
#print net_list
print "Host Count:",len(net_list)
conn.close()



