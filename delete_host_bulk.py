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
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/vnet/host")
r1=conn.getresponse()
data=r1.read()
#out=re.findall(r"\"id\":\"[\d\w-]+\"",data)
id=re.findall(r"[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
#print out
conn.close()
print len(id)
id1=id[::len(id)/4]
id2=id[len(id1)::len(id)/2]
id3=id[len(id1)+len(id2)::]
body1={
       "ids":id1
      }
body2={
        "ids":id2
      }
body3={
        "ids":id3
      }
conn = httplib.HTTPConnection(url, 8181)
conn.request("POST", "/vnet/host/batchdelete", json.dumps(body1), headers)
resp=conn.getresponse()
if resp is not None:
  print resp.status, resp.reason
  data = resp.read()
  print data
conn.close()
conn = httplib.HTTPConnection(url, 8181)
conn.request("POST", "/vnet/host/batchdelete", json.dumps(body2), headers)
resp=conn.getresponse()
if resp is not None:
  print resp.status, resp.reason
  data = resp.read()
  print data
conn.close()
conn = httplib.HTTPConnection(url, 8181)
conn.request("POST", "/vnet/host/batchdelete", json.dumps(body3), headers)
resp=conn.getresponse()
if resp is not None:
  print resp.status, resp.reason
  data = resp.read()
  print data
conn.close()



