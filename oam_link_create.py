# /usr/bin/
import sys
import httplib
import json
import re
import time

def CLI(filename):
  c=[]
  fhandler=open(filename,'r')
  cli=list(fhandler) 
  for i in cli:
    c.append(i[:-1])
  return c

def KEY(value):
  o=re.split('\.',value)
  return int(o[-1])
    
c=0
bdy=[]
data=[]
dev_data={}
asw_dev_ip=CLI('asw_dev_ip')
asw_dev_ip.sort(key=KEY)
dsw_dev_ip=CLI('dsw_dev_ip')
dsw_dev_ip.sort(key=KEY)
dst_asw=sorted(asw_dev_ip,key=KEY,reverse=True)
asw_vtep=CLI('asw_vtep')
asw_vtep.sort(key=KEY)
dst_vtep=sorted(asw_vtep,key=KEY,reverse=True)
dsw_vtep=CLI('dsw_vtep')
vni=CLI('vni')
#print asw_dev_ip
url = '172.25.241.50'
for a in range(0,len(asw_dev_ip)):
  if (c==2) :
    c=0
  datum=[asw_vtep[a],dsw_vtep[c],vni[c],dst_vtep[a],dst_asw[a]]
  c=c+1
  data.append(datum)

dev_data=dict(zip(asw_dev_ip,data))
#print dev_data
headers = {
    "Content-type": "application/json"
}
for org_dev_ip,val in dev_data.items():
    body = {
            "link_detect_task":
            {
              "origin_device" : org_dev_ip,
              "origin_vtep" : val[0],
         
              "dest_device" : val[-1],
              "dest_vtep" : val[-2],
         
              "vni" : val[2],
         
              "samples" : 200,
         
              "timeout" : 50,
         
              "persistent_time" : 5

            }
          }
    print  body
    conn = httplib.HTTPConnection(url, 8181)
    conn.request("POST", "/oam/link_detect_task", json.dumps(body), headers)
    response=conn.getresponse()
    if response is not None:
        print response.status, response.reason
        data = response.read()
        print data
    conn.close()
