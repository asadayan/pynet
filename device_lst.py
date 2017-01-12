# /usr/bin/
import sys
import httplib
import urllib
import json
import re

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
conn.request("GET", "/vnet/device/")
r1=conn.getresponse()
data=r1.read()
id=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
out=re.split('name',data)
dev=re.findall(r"[ADP]SW...",data)
z=dict(zip(dev,id))
if not id:
  print "No Devices Created"
  sys.exit()
conn.close()
for i in out:
  print i,'\n\n'

