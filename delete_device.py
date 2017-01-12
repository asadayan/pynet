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

dev=re.findall(r"[ADP]SW...",data)
z=dict(zip(dev,id))
if not id:
  print "No Devices Created"
  sys.exit()
conn.close()

for d,i in z.items():
  body={
         "id":i
        }
  path="/vnet/device/"+i
  print "Deleting Device..",d,i
  conn = httplib.HTTPConnection(url, 8181)
  conn.request("DELETE",path)
  resp=conn.getresponse()
  if resp is not None:
    print resp.status, resp.reason
    data = resp.read()
    print data
conn.close()



